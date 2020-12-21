# -*- coding: utf-8 -*-
from core.utils import time_by_adding_business_days
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer
from .gsx_validate import gsx_validate


class DiagnosticsStatusSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField()

    def validate_identifier(self, value):
        """
        Check that device identifier is valid.
        """
        is_valid_alternate_device_id = gsx_validate(value, "alternateDeviceId")
        is_valid_sn = gsx_validate(value, "serialNumber")
        if not is_valid_alternate_device_id and not is_valid_sn:
            raise serializers.ValidationError(
                "Not a valid serial number or IMEI number."
            )
        return value

    def create(self, validated_data):
        req = GSXRequest(
            "diagnostics",
            "status",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {"id": validated_data["identifier"]}
        response = req.post(device=device)
        return response
