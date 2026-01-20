from django.contrib.auth.models import AbstractUser
from apps.core.models import TenantAwareModel

class User(AbstractUser, TenantAwareModel):
    pass
