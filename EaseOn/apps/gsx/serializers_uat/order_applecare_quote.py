from .base_gsx_serializer import BaseGSXSerializerUAT
from rest_framework import serializers
from gsx.core import GSXRequestUAT
import copy


def get_dummay_payload():
    return   {

    "partNumber": "S4517ZM/A",
   "device": {
    "id": "511113481600080"
    }

 }



class OrderAppleCareQuoteSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "order",
            "applecare/quote",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
