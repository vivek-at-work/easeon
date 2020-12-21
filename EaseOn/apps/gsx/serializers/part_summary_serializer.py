# -*- coding: utf-8 -*-
import copy

from core.utils import time_by_adding_business_days
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer
from .gsx_validate import gsx_validate


class PartSummarySerializer(BaseGSXSerializer):
    search_criteria = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "parts",
            "summary",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data["search_criteria"])
        response = req.post(**data)
        return response
