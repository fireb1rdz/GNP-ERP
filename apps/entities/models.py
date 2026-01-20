from django.db import models
from apps.core.models import TenantAwareModel
from django.utils.text import slugify

class Entity(TenantAwareModel):
    choices = {
        'CPF': 'CPF',
        'CNPJ': 'CNPJ',
    }
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)
    cpfoucnpj = models.CharField(max_length=4, choices=choices.items(), default='CPF')
    is_active = models.BooleanField(default=True)
    is_client = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_member_of_tenant = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False, help_text='Allow access to the entity as system company')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.cpf:
            self.cpfoucnpj = self.choices['CPF']
        else:
            self.cpfoucnpj = self.choices['CNPJ']
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'
        ordering = ['name']
