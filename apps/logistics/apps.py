from django.apps import AppConfig


app_name = "logistics"
class LogisticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.logistics'
    verbose_name = 'Logistics'
    
    def ready(self): 
        from apps.logistics.services.conference_service import ConferenceService
        from domain.registry.module_registry import ModuleRegistry
        ModuleRegistry.register(
            namespace="logistics",
            service_instance=ConferenceService,
        )
