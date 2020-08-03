# -*- coding: utf-8 -*-
from core.utils import time_by_adding_business_days
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class WarrantySerializer(BaseGSXSerializer):
    """
    Warranty Serializer
    """

    service = 'repair'
    action = 'product/details?activationDetails=true'
    identifier = serializers.CharField(validators=[validate_device_identifier])
    unitReceivedDateTime = serializers.CharField(
        default=time_by_adding_business_days(0).isoformat()
    )
