from django.apps import AppConfig

class FiscalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.fiscal'
    verbose_name = 'Fiscal'
    
    def ready(self):
        from apps.core.services.base import ModuleRegistry
        from apps.fiscal.services import FiscalService
        ModuleRegistry.register('fiscal', FiscalService())