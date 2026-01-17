from django.apps import AppConfig
from apps.core.services import ModuleRegistry

class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.finance'

    def ready(self):
        # Register the Finance Service implementation
        from .services import FinanceServiceImpl
        ModuleRegistry.register('finance', FinanceServiceImpl())
