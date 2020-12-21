# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequestUAT
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializerUAT


def get_dummay_payload():
    return {
        "issueType": "SIG",
        "escalationTypeCode": "GSXHELP",
        "notes": [
            {
                "type": "ESCALATION",
                "content": "You’ll move the world forward. Every day, we create the most innovative mapping and location technologies to shape tomorrow’s mobility for the better.",
            }
        ],
        "context": [{"contextType": "IMEI_NO", "id": "451142410360030"}],
        "escalateTo": "APPLE",
        "shipTo": "0001026647",
    }


class EscalationCreateSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "escalation",
            "create",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
