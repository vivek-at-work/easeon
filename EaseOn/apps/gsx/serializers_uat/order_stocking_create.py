from .base_gsx_serializer import BaseGSXSerializerUAT
from rest_framework import serializers
from gsx.core import GSXRequestUAT
import copy


def get_dummay_payload():
    return   {
  "purchaseOrderNumber": "DL66103997",
  "shipToCode": "0001026647",
  "parts": [
    {
      "number": "661-03997",
      "quantity": 1
    }
  ],
  "action": "SAVE"
}





class StockingOrderCreateSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "order",
            "stocking/create",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
