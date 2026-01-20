from django.apps import AppConfig

class EntitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.entities'
    verbose_name = 'Entities'
    
    def ready(self):
        from apps.core.services.base import ModuleRegistry
        from apps.entities.services import EntityService
        ModuleRegistry.register('entities', EntityService())