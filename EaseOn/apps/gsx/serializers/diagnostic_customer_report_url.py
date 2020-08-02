# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from .base_serializer import BaseGSXSerializer
from rest_framework import serializers
from .validators import validate_device_identifier


class DiagnosticsReportDownloadSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    eventNumber = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            'diagnostics',
            'customer-report-url',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        response = req.post(**validated_data)
        return response
