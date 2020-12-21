# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer


class RepairCreateSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    data = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "repair",
            "create",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        if "meta" in self.validated_data["data"]:
            del self.validated_data["data"]["meta"]
        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
