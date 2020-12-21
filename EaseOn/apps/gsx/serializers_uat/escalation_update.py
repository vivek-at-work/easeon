

from .base_gsx_serializer import BaseGSXSerializerUAT
from rest_framework import serializers
from gsx.core import GSXRequestUAT
import copy


def get_dummay_payload():
    return {
  "escalationId": "10000154302621",
  "notes": [
    {
      "content": "string"
    }
  ],
  "escalationStatusCode": "CLOSED",
  "escalateTo": "APPLE",
}


class EscalationUpdateSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "escalation",
            "update",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response

