# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class ConsignmentDeliveryLookupSerializer(BaseGSXSerializer):
    """
    ConsignmentDeliveryLookupSerializer
    """

    service = 'consignment'
    action = 'delivery/lookup'
    pageSize = serializers.CharField(default='50')
    pageNumber = serializers.CharField(default='1')
