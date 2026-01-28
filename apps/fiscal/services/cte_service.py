from apps.fiscal.services.base import FiscalServiceInterface
from fiscal.dto import CTEDTO
from apps.entities.services import EntityService, EntityAddressService

import xml.etree.ElementTree as ET
from decimal import Decimal
from django.utils.dateparse import parse_datetime, parse_date


NS = {
    "cte": "http://www.portalfiscal.inf.br/cte",
    "nfe": "http://www.portalfiscal.inf.br/nfe",
}


def _get_text(node, path, default=None):
    el = node.find(path, NS)
    return el.text.strip() if el is not None and el.text else default


def _get_decimal(node, path, default=Decimal("0.00")):
    value = _get_text(node, path)
    return Decimal(value) if value else default


class CTEService(FiscalServiceInterface):
   