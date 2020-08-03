# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class ConsignmentValidateSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """
    service = 'consignment'
    action = 'validate'
    shipTo = serializers.CharField()
