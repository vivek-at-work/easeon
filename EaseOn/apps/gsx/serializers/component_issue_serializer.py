# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer


class ComponentIssueSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    data = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "repair",
            "product/componentissue",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data["data"])
        response = req.post(**data)
        return response
