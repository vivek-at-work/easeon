# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class RepairEligibilitySerializer(BaseGSXSerializer):
    """
    RepairEligibilitySerializer
    """

    service = 'repair'
    action = 'eligibility'
    identifier = serializers.CharField(validators=[validate_device_identifier])
