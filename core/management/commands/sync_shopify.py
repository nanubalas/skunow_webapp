from django.core.management.base import BaseCommand
from core.models import Tenant
from core.services.sync_shopify import sync_shopify_for_tenant

class Command(BaseCommand):
    help = "Sync Shopify orders + inventory snapshot (MVP/fake fetch)."

    def handle(self, *args, **kwargs):
        for tenant in Tenant.objects.all():
            msg = sync_shopify_for_tenant(tenant)
            self.stdout.write(f"{tenant.name}: {msg}")
