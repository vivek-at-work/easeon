

from .base_gsx_serializer import BaseGSXSerializerUAT
from rest_framework import serializers
from gsx.core import GSXRequestUAT
import copy


def get_dummay_payload():
    return  {

  "action": "SAVE",
  "partNumber": "S4517ZM/A",
  "device": {
    "id": "511113481600090"
    },
  "customer": {
    "firstName": "string",
    "lastName": "string",
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
        "line1": "string"
      }
          ],
    "companyName": "string"
  }

 }



class OrderAppleCareCreateSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "order",
            "applecare/create",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
