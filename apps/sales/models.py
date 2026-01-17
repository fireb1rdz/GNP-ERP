from django.db import models
from apps.core.models import OrganizationAwareModel
from apps.core.services import ModuleRegistry

class Order(OrganizationAwareModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('CONFIRMED', 'Confirmed'),
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    def confirm(self):
        """
        Business logic to confirm order.
        Explicitly calls Finance service via Registry.
        """
        if self.status == 'CONFIRMED':
            return
        
        self.status = 'CONFIRMED'
        self.save()

        # Decoupled Call!
        # If finance is not installed, this returns None (NullService) and does nothing.
        # If installed, it creates the invoice.
        finance_service = ModuleRegistry.get('finance')
        finance_service.create_invoice(
            organization=self.organization,
            amount=self.total,
            reference=f"Order-{self.id}",
            description=f"Invoice for Order {self.id}"
        )
