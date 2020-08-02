# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from .base_serializer import BaseGSXSerializer
from rest_framework import serializers
from .validators import validate_device_identifier


class RunDiagnosticsSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField(validators=[validate_device_identifier])
    suiteId = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            'diagnostics',
            'initiate-test',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        diagnostics = {'suiteId': validated_data['suiteId']}
        response = req.post(device=device, diagnostics=diagnostics,)
        return response
