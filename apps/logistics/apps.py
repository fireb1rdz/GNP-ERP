from django.apps import AppConfig

class LogisticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.logistics'
    verbose_name = 'Logistics'
    
    def ready(self):
        from apps.core.services.base import ModuleRegistry
        from apps.logistics.services import LogisticsService
        ModuleRegistry.register('logistics', LogisticsService())