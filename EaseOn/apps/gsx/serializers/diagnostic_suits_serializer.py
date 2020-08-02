# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from .base_serializer import BaseGSXSerializer
from rest_framework import serializers
from .validators import validate_device_identifier


class DiagnosticSuitesSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField(validators=[validate_device_identifier])

    def create(self, validated_data):
        req = GSXRequest(
            'diagnostics',
            'suites',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        response = req.get(
            deviceId=validated_data['identifier'])
        return response
