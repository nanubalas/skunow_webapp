"""Generate any due recurring invoices. Schedule this daily (cron / Task
Scheduler): ``python manage.py run_recurring_invoices``."""
from django.core.management.base import BaseCommand

from core.services import recurring


class Command(BaseCommand):
    help = "Generate customer invoices from recurring-invoice templates that are due."

    def handle(self, *args, **options):
        created = recurring.generate_due()
        self.stdout.write(self.style.SUCCESS(f"Generated {len(created)} recurring invoice(s)."))
