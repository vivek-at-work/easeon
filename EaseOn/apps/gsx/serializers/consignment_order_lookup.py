# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class ConsignmentOrderLookupSerializer(BaseGSXSerializer):
    """
    DiagnosticsLookupSerializer
    """

    service = 'consignment'
    action = 'order/lookup'
    pageSize = serializers.CharField(default='50')
    pageNumber = serializers.CharField(default='1')
    createdToDate = serializers.CharField(required=False)
    orderId = serializers.CharField(required=False)
    createdFromDate = serializers.CharField(required=False)
    partNumber = serializers.CharField(required=False)
    poNumber = serializers.CharField(required=False)
    orderStatusGroupCode = serializers.CharField(required=False)
    typeCode = serializers.CharField(required=False)
    shipTo = serializers.CharField(required=False)
