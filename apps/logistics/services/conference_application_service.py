# apps/conference/services.py
import xml.etree.ElementTree as ET
from django.utils.timezone import now

from apps.logistics.models import Conference, ConferenceItem
from domain.contracts.stock import PackageServiceInterface
from domain.registry.module_registry import ModuleRegistry
from domain.contracts.logistics import ConferenceServiceInterface
from domain.dto.fiscal import CTEDTO

class ConferenceApplicationService:
    def __init__(self, package_service: PackageServiceInterface):
        self.package_service = package_service

    def create_from_access_key(self, tenant, user, origin, destination, event_type, access_key):
        conference = Conference.objects.create(
            tenant=tenant,
            user=user,
            origin=origin,
            destination=destination,
            event_type=event_type,
            document_number=access_key,
            document_type="invoice"
        )
        return conference

    def create_from_dto(self, tenant, user, supplier, carrier, client, dto: CTEDTO):
        for nfe in dto.related_nfes:
            conference = Conference.objects.create(
                tenant=tenant,
                supplier=supplier,
                carrier=carrier,
                client=client,
                document_number=nfe.access_key,
                status="pending",
                created_by=user,
            )

        self.create_items_from_dto(
            tenant=tenant,
            conference=conference,
            dto=dto,
        )

    def create_items_from_dto(self, tenant, conference, dto):
        for _ in range(dto.quantity):
            package = self.package_service.create_generated_package(
                tenant=tenant,
                product_description=dto.description,
            )

            ConferenceItem.objects.create(
                tenant=tenant,
                conference=conference,
                package=package,
                status="pending",
            )
