from domain.contracts.entity import PartyServiceInterface
from apps.entities.models import Entity, PartyRole

class PartyService(PartyServiceInterface):
    def create_party(self, tenant, party_data):
        pass
    
    def get_or_create_party(self, tenant, party_data):
        pass

    def update_party(self, tenant, party_id, party_data):
        pass

    def delete_party(self, tenant, party_id):
        pass

    def list_parties(self, tenant):
        pass

    def get_party(self, tenant, party_id):
        pass

    def can_be(self, entity: Entity, role: str):
        """
        Verifica se a entity pode ser um party.
        """
        return True

    def get_roles(self, entity: Entity):
        """
        Retorna os papéis da entity.
        """
        pass

    def get_existing_roles(self):
        """
        Retorna os papéis existentes da entity.
        """
        roles = []
        for role, translation in PartyRole.choices:
            roles.append((role, translation))
        return roles