from django.db import models
from apps.core.models import TenantAwareModel
from apps.entities.services 

class Package(TenantAwareModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    tracking_code = models.CharField(max_length=255)
    stock = models.IntegerField() # Integrar posteriormente com o sistema de estoque
    