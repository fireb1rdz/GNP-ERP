import uuid
from django.db import models, connection
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import get_tenant_model


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tenant(TenantMixin, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    value_per_read_package = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    default_due_day = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    def has_module(self, module_name):
        return self.tenant_modules.filter(module__name=module_name).exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug or str(self.id)
        super().save(*args, **kwargs)


class Domain(DomainMixin):
    pass


class TenantAwareModel(TimeStampedModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="%(class)s_tenant"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            schema_name = getattr(connection, "schema_name", None)
            if not schema_name:
                raise RuntimeError("Nenhum schema ativo no contexto da conexão")

            TenantModel = get_tenant_model()
            real_tenant = TenantModel.objects.filter(schema_name=schema_name).first()

            if real_tenant is None:
                raise RuntimeError(
                    f"Nenhum tenant encontrado para o schema '{schema_name}'"
                )

            self.tenant = real_tenant

        super().save(*args, **kwargs)


class Module(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TenantModule(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tenant_modules")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="tenant_modules")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.module}"