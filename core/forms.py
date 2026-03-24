from django import forms
from django.forms import inlineformset_factory
from core.models import (
    CycleCount, CycleCountLine, InventoryLotBalance, InventoryReservation,
    PurchaseOrder, PurchaseOrderLine, Shipment,
    Product, Supplier, Location, ChannelConnection,
    SalesOrder, SalesOrderLine, Tenant,
    UnitOfMeasure, UOMConversion, BillOfMaterials, BillOfMaterialsLine, ProductBarcode,
    InventoryTransfer, InventoryTransferLine,
    GoodsReceipt, GoodsReceiptLine, LandedCostCharge,
    SupplierInvoice, SupplierInvoiceLine,
    TaxCode, Customer, CustomerInvoice, CustomerInvoiceLine, GLAccount
)

class PurchaseOrderForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save", "Save Draft"), ("submit", "Submit PO")),
        required=False
    )

    class Meta:
        model = PurchaseOrder
        fields = ["supplier", "expected_date", "notes"]

PurchaseOrderLineFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderLine,
    fields=("product", "ordered_qty", "unit_cost"),
    extra=1,
    can_delete=True
)

class ShipmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["carrier", "tracking_number", "status"]

class ProductForm(forms.ModelForm):
    barcode = forms.CharField(required=False, help_text="Optional EAN/UPC/Barcode")

    class Meta:
        model = Product
        fields = ["parent", "sku", "name", "variant_name", "option1", "option2", "option3",
                  "base_uom", "uom", "cost_method", "standard_cost"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name","email","phone","currency_code"]

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "type"]

class ChannelConnectionForm(forms.ModelForm):
    class Meta:
        model = ChannelConnection
        fields = ["channel", "name", "shop_domain", "access_token"]
        widgets = {
            "access_token": forms.Textarea(attrs={"rows": 3}),
        }

class SalesOrderForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save", "Save Draft"), ("post", "Post (deduct inventory)")),
        required=False
    )
    class Meta:
        model = SalesOrder
        fields = ["channel", "order_number", "order_date", "ship_from_location"]  # header default; lines can override

SalesOrderLineFormSet = inlineformset_factory(
    SalesOrder,
    SalesOrderLine,
    fields=("product", "ship_from_location", "qty", "unit_price", "lot_code", "serial_number", "expiry_date"),
    extra=1,
    can_delete=True
)

class TenantSettingsForm(forms.ModelForm):
    CURRENCY_CHOICES = (
        ("GBP", "GBP (£)"),
        ("USD", "USD ($)"),
        ("EUR", "EUR (€)"),
    )

    currency_code = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = Tenant
        fields = ["name", "currency_code", "po_approval_threshold"]

class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ["code", "name"]


class UOMConversionForm(forms.ModelForm):
    class Meta:
        model = UOMConversion
        fields = ["product", "from_uom", "to_uom", "multiplier"]


class BillOfMaterialsForm(forms.ModelForm):
    class Meta:
        model = BillOfMaterials
        fields = ["product", "name", "is_active"]


BOMLineFormSet = inlineformset_factory(
    BillOfMaterials,
    BillOfMaterialsLine,
    fields=("component", "qty", "uom"),
    extra=1,
    can_delete=True
)


# ---------------- Inventory Controls ----------------

class CycleCountForm(forms.ModelForm):
    class Meta:
        model = CycleCount
        fields = ["location", "count_date", "notes"]

class CycleCountLineForm(forms.ModelForm):
    class Meta:
        model = CycleCountLine
        fields = ["product", "lot_code", "serial_number", "expiry_date", "counted_qty"]

CycleCountLineFormSet = inlineformset_factory(
    CycleCount,
    CycleCountLine,
    form=CycleCountLineForm,
    extra=1,
    can_delete=True
)


# --- Transfers ---
class InventoryTransferForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save","Save Draft"),("post","Post Transfer")),
        required=False
    )
    class Meta:
        model = InventoryTransfer
        fields = ["from_location","to_location","notes"]

InventoryTransferLineFormSet = inlineformset_factory(
    InventoryTransfer,
    InventoryTransferLine,
    fields=("product","qty","lot_code","serial_number","expiry_date"),
    extra=1,
    can_delete=True
)


# --- Goods Receipt (GRN) ---
class GoodsReceiptForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save","Save Draft"),("post","Post GRN")),
        required=False
    )
    class Meta:
        model = GoodsReceipt
        fields = ["grn_number","received_at","received_to","attachment"]

GoodsReceiptLineFormSet = inlineformset_factory(
    GoodsReceipt,
    GoodsReceiptLine,
    fields=("po_line","product","qty_received","unit_cost","lot_code","serial_number","expiry_date"),
    extra=1,
    can_delete=True
)

class LandedCostChargeForm(forms.ModelForm):
    class Meta:
        model = LandedCostCharge
        fields = ["name","amount","currency_code"]


# --- Supplier Invoice (3-way match) ---
class SupplierInvoiceForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save","Save Draft"),("submit","Run Match"),("approve","Approve"),("post","Post")),
        required=False
    )
    class Meta:
        model = SupplierInvoice
        fields = ["supplier","po","receipt","invoice_number","invoice_date","currency_code","attachment"]

SupplierInvoiceLineFormSet = inlineformset_factory(
    SupplierInvoice,
    SupplierInvoiceLine,
    fields=("product","po_line","receipt_line","qty","unit_cost"),
    extra=1,
    can_delete=True
)


from core.models import ReturnAuthorization, ReturnLine

class ReturnAuthorizationForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save", "Save Draft"), ("approve", "Approve"), ("receive", "Receive & Restock")),
        required=False
    )
    class Meta:
        model = ReturnAuthorization
        fields = ["channel", "rma_number", "original_order_number", "receive_location"]

ReturnLineFormSet = inlineformset_factory(
    ReturnAuthorization,
    ReturnLine,
    fields=("product", "qty", "reason", "lot_code", "serial_number", "expiry_date"),
    extra=1,
    can_delete=True
)


class TaxCodeForm(forms.ModelForm):
    class Meta:
        model = TaxCode
        fields = ["code", "name", "rate", "is_active"]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "vat_number", "billing_address"]
        widgets = {"billing_address": forms.Textarea(attrs={"rows": 3})}

class CustomerInvoiceForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("save", "Save Draft"), ("issue", "Issue (Post to GL)")),
        required=False
    )
    class Meta:
        model = CustomerInvoice
        fields = ["customer", "invoice_number", "invoice_date", "due_date", "notes"]

CustomerInvoiceLineFormSet = inlineformset_factory(
    CustomerInvoice,
    CustomerInvoiceLine,
    fields=("product", "description", "qty", "unit_price", "tax_code"),
    extra=1,
    can_delete=True
)

class GLAccountForm(forms.ModelForm):
    class Meta:
        model = GLAccount
        fields = ["code", "name", "type", "is_active"]
