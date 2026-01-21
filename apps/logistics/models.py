from django.db import models
from apps.entities.services 

class Package(models.Model):
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE)
    tracking_code = models.CharField(max_length=255)
    stock = models.IntegerField() # Integrar posteriormente com o sistema de estoque
    

    