# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class ConsignmentValidateSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    shipTo = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            'consignment',
            'validate',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        response = req.post(**validated_data)
        return response
