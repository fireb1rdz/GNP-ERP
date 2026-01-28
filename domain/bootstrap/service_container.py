from domain.contracts.entity import PartyServiceInterface
from apps.entities.services.party_service import PartyService
from domain.contracts.logistics import ConferenceServiceInterface
from apps.logistics.services.conference_service import ConferenceService
from domain.contracts.stock import PackageServiceInterface
from apps.stock.services.package_service import PackageService

def get_party_service() -> PartyServiceInterface:
    return PartyService()

def get_conference_service() -> ConferenceServiceInterface:
    return ConferenceService(get_package_service())

def get_package_service() -> PackageServiceInterface:
    return PackageService()
