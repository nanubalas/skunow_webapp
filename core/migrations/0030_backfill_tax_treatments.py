from decimal import Decimal

from django.db import migrations

# Map existing tax-code codes to a VAT treatment.
CODE_TO_KIND = {
    "STD": "STANDARD",
    "RED": "REDUCED",
    "ZERO": "ZERO",
    "EXEMPT": "EXEMPT",
    "OS": "OUTSIDE",
}

# Codes to ensure exist for every tenant (Reduced + Outside-scope are new).
ENSURE = [
    ("RED", "Reduced rate (5%)", Decimal("0.05"), "REDUCED"),
    ("OS", "Outside the scope of VAT", Decimal("0.00"), "OUTSIDE"),
]


def forwards(apps, schema_editor):
    TaxCode = apps.get_model("core", "TaxCode")
    Tenant = apps.get_model("core", "Tenant")

    # Classify existing codes by their code; rate-0 unknowns default to EXEMPT,
    # positive-rate unknowns to STANDARD.
    for tc in TaxCode.objects.all():
        kind = CODE_TO_KIND.get(tc.code.upper())
        if kind is None:
            kind = "STANDARD" if (tc.rate or Decimal("0")) > 0 else "EXEMPT"
        tc.kind = kind
        tc.save(update_fields=["kind"])

    # Add the new default codes to every tenant that lacks them.
    for tenant in Tenant.objects.all():
        for code, name, rate, kind in ENSURE:
            TaxCode.objects.get_or_create(
                tenant=tenant, code=code,
                defaults={"name": name, "rate": rate, "kind": kind},
            )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("core", "0029_taxcode_kind")]
    operations = [migrations.RunPython(forwards, noop)]
