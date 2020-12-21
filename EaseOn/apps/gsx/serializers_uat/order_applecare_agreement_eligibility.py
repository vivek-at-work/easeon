# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequestUAT
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializerUAT


def get_dummay_payload():
    return {"device": {"id": "511113481600080"}}


class OrderAppleCareAgreementEligibilitySerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "order",
            "applecare/agreementEligibility",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
