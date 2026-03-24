# SKUNOW Webapp (Phase 1 + Phase 2 MVP)

This is a Django server-rendered MVP for:
- Purchase Orders (Draft/Submit)
- Shipments (basic tracking fields)
- Receiving (GRN) with partial receipts
- Inventory balances updated via immutable movement ledger
- Shopify sync *pattern* (fake fetch): orders -> SALE movements, snapshot stored read-only
- Reconciliation page: Shopify snapshot vs SKUNOW totals

## Quick start (Windows / Mac / Linux)

### 1) Create venv and install deps
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Run migrations and create admin user
```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
```

### 3) Start server
```bash
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/po/ (PO list)
- http://127.0.0.1:8000/admin/ (Admin)

## Seed minimum data in Admin
In **Admin** create:
1) Tenant (e.g. SKUNOW)
2) Location (e.g. Main Warehouse)
3) Supplier
4) Products with SKUs: SKU-001, SKU-002
5) ChannelConnection: channel=SHOPIFY (token/domain optional for now)

## Test Phase 1
- Create PO: /po/new/
- Submit PO (creates a Shipment using your first Location)
- Receive PO: open the PO and click Receive, then enter quantities
- Check inventory: /inventory/

## Test Phase 2 (Shopify sync - fake fetch)
Run:
```bash
python manage.py sync_shopify
```

This will:
- Create SALE movements for the fake order
- Store Shopify snapshot rows
- View reconciliation at: /reconcile/

## Notes
- For demo speed this uses the **first Tenant** as the active tenant.
- Next step for production: tie tenant to user login + role-based access.
