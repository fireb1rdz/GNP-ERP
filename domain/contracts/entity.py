from abc import ABC, abstractmethod
from apps.entities.models import Entity

class EntityServiceInterface(ABC):
    @abstractmethod
    def create_entity(self, tenant, entity_data):
        pass
    
    @abstractmethod
    def get_or_create(self, tenant, entity_data):
        pass

    @abstractmethod
    def update_entity(self, tenant, entity_id, entity_data):
        pass

    @abstractmethod
    def delete_entity(self, tenant, entity_id):
        pass

    @abstractmethod
    def list_entities(self, tenant):
        pass

    @abstractmethod
    def get_entity(self, tenant, entity_id):
        pass

class EntityAddressServiceInterface(ABC):
    @abstractmethod
    def create_entity_address(self, tenant, entity_id, entity_address_data):
        pass
    
    @abstractmethod
    def get_or_create_entity_address(self, tenant, entity_id, entity_address_data):
        pass

    @abstractmethod
    def update_entity_address(self, tenant, entity_id, entity_address_id, entity_address_data):
        pass

    @abstractmethod
    def delete_entity_address(self, tenant, entity_id, entity_address_id):
        pass

    @abstractmethod
    def list_entity_addresses(self, tenant, entity_id):
        pass

    @abstractmethod
    def get_entity_address(self, tenant, entity_id, entity_address_id):
        pass

class PartyServiceInterface(ABC):
    @abstractmethod
    def create_party(self, tenant, party_data):
        pass
    
    @abstractmethod
    def get_or_create_party(self, tenant, party_data):
        pass

    @abstractmethod
    def update_party(self, tenant, party_id, party_data):
        pass

    @abstractmethod
    def delete_party(self, tenant, party_id):
        pass

    @abstractmethod
    def list_parties(self, tenant):
        pass

    @abstractmethod
    def get_party(self, tenant, party_id):
        pass

    @abstractmethod
    def can_be(self, entity: Entity, role: str):
        """
        Verifica se a entity pode ser um party.
        """
        pass

    @abstractmethod
    def get_roles(self, entity: Entity):
        """
        Retorna os papéis da entity.
        """
        pass

    @abstractmethod
    def get_existing_roles(self):
        """
        Retorna os papéis padrão da entity.
        """
        pass