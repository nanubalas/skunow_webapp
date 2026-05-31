from django.db import migrations


def add_ppv_account(apps, schema_editor):
    Tenant = apps.get_model("core", "Tenant")
    GLAccount = apps.get_model("core", "GLAccount")
    for tenant in Tenant.objects.all():
        GLAccount.objects.get_or_create(
            tenant=tenant, code="5100",
            defaults={"name": "Purchase Price Variance", "type": "EXPENSE", "is_active": True},
        )


def remove_ppv_account(apps, schema_editor):
    GLAccount = apps.get_model("core", "GLAccount")
    GLAccount.objects.filter(code="5100", name="Purchase Price Variance").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_backfill_accruals_account"),
    ]
    operations = [
        migrations.RunPython(add_ppv_account, remove_ppv_account),
    ]
