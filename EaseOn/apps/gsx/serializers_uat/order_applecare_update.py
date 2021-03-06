# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequestUAT
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializerUAT


def get_dummay_payload():
    return {
        "orderId": "GA1000008727",
        "proofOfCoverageEmailLanguage": "ENG",
        "action": "CONFIRM",
        "purchaseOrderNumber": "FC1234",
        "partNumber": "S4517ZM/A",
        "device": {"id": "511113481600080"},
        "customer": {
            "firstName": "Vivek",
            "lastName": "Srivastava",
            "primaryPhone": "9657946755",
            "emailAddress": "ervivek.rbl@gmail.com",
            "address": [
                {
                    "city": "string",
                    "countryCode": "IND",
                    "postalCode": "411007",
                    "stateCode": "D",
                    "line3": "string",
                    "line2": "string",
                    "line1": "string",
                }
            ],
            "companyName": "string",
        },
    }


class OrderAppleCareUpdateSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "order",
            "applecare/update",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
