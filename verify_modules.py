# verify_modules.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Organization
from apps.sales.models import Order
from apps.finance.models import Invoice

def run():
    print("--- Starting Verification ---")
    
    # 1. Create Tenant
    org, created = Organization.objects.get_or_create(
        name="Tech Corp", 
        slug="tech-corp"
    )
    print(f"[Core] Organization: {org.name}")

    # 2. Create Order (Sales)
    order = Order.objects.create(
        organization=org,
        total=1500.00
    )
    print(f"[Sales] Order Created: ID {order.id}, Status: {order.status}")

    # 3. Confirm Order (Triggers Finance via Registry)
    print("[Sales] Confirming Order...")
    order.confirm()
    print(f"[Sales] Order Status: {order.status}")

    # 4. Verify Invoice (Finance)
    invoices = Invoice.objects.filter(source_reference=f"Order-{order.id}")
    if invoices.exists():
        inv = invoices.first()
        print(f"[Finance] SUCCESS: Invoice found! ID {inv.id}, Amount: {inv.amount}")
    else:
        print("[Finance] FAILURE: No invoice generated.")

if __name__ == '__main__':
    run()
