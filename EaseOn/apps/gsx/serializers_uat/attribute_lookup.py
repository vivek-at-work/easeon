# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequestUAT
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializerUAT


def get_dummay_payload():
    return {"attributes": [{"type": "ESC_TYPE_ISSUECATEGORIES_MAP", "key": "GSXHELP"}]}


class AttributeLookupSerializer(BaseGSXSerializerUAT):
    """
    AttributeLookupSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "attribute",
            "lookup",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
