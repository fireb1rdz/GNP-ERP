from django.apps import AppConfig
from apps.fiscal.factory import DocumentImporterRegistry
from apps.fiscal.importers.cte import CTEImporter

class FiscalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.fiscal'
    verbose_name = 'Fiscal'
    
    def ready(self):
        from apps.core.services.base import ModuleRegistry
        from apps.fiscal.services import FiscalService
        ModuleRegistry.register('fiscal', FiscalService())
        DocumentImporterRegistry.register(CTEImporter())
