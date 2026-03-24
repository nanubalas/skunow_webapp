from django.contrib import admin
from core.models import (
    Tenant, Location, Supplier, Product,
    PurchaseOrder, PurchaseOrderLine,
    Shipment, ShipmentEvent,
    InventoryBalance, InventoryMovement,
    ChannelConnection, SyncRun, ChannelSnapshot, ChannelOrder,
    UnitOfMeasure, UOMConversion, ProductBarcode, BillOfMaterials, BillOfMaterialsLine,
    TaxCode, Customer, CustomerInvoice, CustomerInvoiceLine,
    GLAccount, JournalEntry, JournalLine
)

admin.site.register(Tenant)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
admin.site.register(Shipment)
admin.site.register(ShipmentEvent)
admin.site.register(InventoryBalance)
admin.site.register(InventoryMovement)
admin.site.register(ChannelConnection)
admin.site.register(SyncRun)
admin.site.register(ChannelSnapshot)
admin.site.register(ChannelOrder)

admin.site.register(UnitOfMeasure)
admin.site.register(UOMConversion)
admin.site.register(ProductBarcode)
admin.site.register(BillOfMaterials)
admin.site.register(BillOfMaterialsLine)

admin.site.register(TaxCode)
admin.site.register(Customer)
admin.site.register(CustomerInvoice)
admin.site.register(CustomerInvoiceLine)
admin.site.register(GLAccount)
admin.site.register(JournalEntry)
admin.site.register(JournalLine)
