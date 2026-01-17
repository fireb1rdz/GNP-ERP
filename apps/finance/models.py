from django.db import models
from apps.core.models import OrganizationAwareModel

class Invoice(OrganizationAwareModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)
    # Storing external reference loosely (e.g. "Order #123") instead of ForeignKey
    # to maintain loose coupling.
    source_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.amount}"
