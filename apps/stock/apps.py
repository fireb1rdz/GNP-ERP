from django.apps import AppConfig

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    verbose_name = 'Stock'
    
    def ready(self):
        from apps.core.services.base import ModuleRegistry
        from apps.stock.services import StockService
        ModuleRegistry.register('stock', StockService())