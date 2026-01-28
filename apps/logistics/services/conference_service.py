# apps/conference/services.py
import xml.etree.ElementTree as ET
from django.utils.timezone import now

from apps.logistics.models import Conference, ConferenceItem
from domain.contracts.stock import PackageServiceInterface
from domain.registry.module_registry import ModuleRegistry
from domain.contracts.logistics import ConferenceServiceInterface


class ConferenceService(ConferenceServiceInterface):
    def __init__(self, package_service: PackageServiceInterface):
        self.package_service = package_service

    def create_from_source(self, *, tenant, user, source_files):
        fiscal = ModuleRegistry.get("fiscal")

        if not fiscal:
            raise RuntimeError("Módulo fiscal não disponível")

        for xml in source_files:
            source = fiscal.import_document(xml)

            conference = Conference.objects.create(
                tenant=tenant,
                source_entity=source.supplier,
                shipping_entity=source.carrier,
                destination_entity=source.client,
                invoice=source.id,
                status="pending",
                created_by=user,
            )

            self.create_items_from_source(
                tenant=tenant,
                conference=conference,
                source=source,
            )

    def create_items_from_source(self,*, tenant, conference, source):
        """
        Para cada volume/produto da NF:
        - cria um Package
        - gera tracking_code sequencial
        - cria ConferenceItem
        """


        for item in source.iter_items():
            # Se o documento não tiver volume, assume 1
            quantity = item.quantity or 1

            for _ in range(quantity):
                package = self.package_service.create_generated_package(
                    tenant=tenant,
                    product_description=item.description,
                )

                ConferenceItem.objects.create(
                    tenant=tenant,
                    conference=conference,
                    package=package,
                    status="pending",
                )
