"""Generation of customer invoices from recurring-invoice templates."""
import datetime

from django.utils import timezone

SAFETY_CAP = 120  # max invoices generated per template per run (catch-up guard)


def add_months(d, n):
    """Add n calendar months to a date, clamping the day to the month length."""
    month_index = d.month - 1 + n
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    # Clamp day (e.g. 31 Jan + 1 month -> 28/29 Feb).
    if month == 12:
        next_month_first = datetime.date(year + 1, 1, 1)
    else:
        next_month_first = datetime.date(year, month + 1, 1)
    last_day = (next_month_first - datetime.timedelta(days=1)).day
    return datetime.date(year, month, min(d.day, last_day))


def advance(d, frequency, interval):
    interval = max(int(interval or 1), 1)
    if frequency == "WEEKLY":
        return d + datetime.timedelta(weeks=interval)
    if frequency == "MONTHLY":
        return add_months(d, interval)
    if frequency == "QUARTERLY":
        return add_months(d, 3 * interval)
    if frequency == "YEARLY":
        return add_months(d, 12 * interval)
    return add_months(d, interval)


def _finished(template):
    if template.max_occurrences and template.occurrences >= template.max_occurrences:
        return True
    if template.end_date and template.next_run_date > template.end_date:
        return True
    return False


def generate_for_template(template, today=None, user=None):
    """Generate any invoices now due for a single template; returns the list."""
    from core.models import CustomerInvoice, CustomerInvoiceLine
    from core.numbering import next_invoice_number
    from core.services.gl import post_customer_invoice

    today = today or timezone.localdate()
    created = []
    if not template.is_active:
        return created

    guard = 0
    while template.is_active and not _finished(template) and template.next_run_date <= today and guard < SAFETY_CAP:
        guard += 1
        run_date = template.next_run_date
        inv = CustomerInvoice.objects.create(
            tenant=template.tenant, customer=template.customer,
            invoice_number=next_invoice_number(template.tenant),
            invoice_date=run_date, currency_code=template.currency_code,
            notes=template.notes, terms=template.terms)
        terms_days = template.tenant.default_payment_terms_days
        if terms_days:
            inv.due_date = run_date + datetime.timedelta(days=terms_days)
            inv.save(update_fields=["due_date"])
        for l in template.lines.all():
            CustomerInvoiceLine.objects.create(
                invoice=inv, product=l.product, description=l.description, qty=l.qty,
                unit_price=l.unit_price, discount_pct=l.discount_pct, tax_code=l.tax_code)
        if template.auto_issue:
            post_customer_invoice(inv, user=user)
        created.append(inv)

        template.occurrences += 1
        template.next_run_date = advance(template.next_run_date, template.frequency, template.interval)
        if _finished(template):
            template.is_active = False
    template.last_run_at = timezone.now()
    template.save(update_fields=["occurrences", "next_run_date", "is_active", "last_run_at"])
    return created


def generate_due(tenant=None, today=None, user=None):
    """Generate due invoices for all active templates (optionally one tenant)."""
    from core.models import RecurringInvoice
    qs = RecurringInvoice.objects.filter(is_active=True)
    if tenant is not None:
        qs = qs.filter(tenant=tenant)
    created = []
    for template in qs.select_related("tenant", "customer").prefetch_related("lines", "lines__tax_code"):
        created.extend(generate_for_template(template, today=today, user=user))
    return created
