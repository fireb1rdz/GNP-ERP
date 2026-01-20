from .models import Entity
from apps.core.services.entities import EntityServiceInterface

class EntityService(EntityServiceInterface):
    def create_entity(self, tenant, data):
        entity = Entity.objects.create(tenant=tenant, **data)
        return entity

    def update_entity(self, entity, data):
        entity.update(**data)
        return entity

    def delete_entity(self, entity):
        entity.delete()
        return entity

    def list_entities(self, tenant):
        return Entity.objects.filter(tenant=tenant)

    def get_entity(self, tenant, entity_id):
        return Entity.objects.get(tenant=tenant, id=entity_id)

    