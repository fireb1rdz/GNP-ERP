import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Organization(TimeStampedModel):
    """
    The Tenant. Each customer is an Organization.
    Modules can be enabled/disabled per organization (feature flags).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    
    # Simple JSON field to store active modules, e.g., ["sales", "finance"]
    # In a real SaaS, this might be a separate relation or License model.
    active_modules = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class OrganizationAwareModel(TimeStampedModel):
    """
    Mixin for models that belong to a specific tenant.
    """
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="%(class)s_set"
    )

    class Meta:
        abstract = True
