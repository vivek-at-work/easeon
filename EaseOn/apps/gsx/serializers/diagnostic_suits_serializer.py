# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class DiagnosticSuitesSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    service = 'diagnostics'
    action = 'suites'
    http_verb = 'GET'
    identifier = serializers.CharField(validators=[validate_device_identifier])

    def get_payload(self, validated_data):
        payload = {}
        payload['deviceId'] = validated_data['identifier']
        return payload
