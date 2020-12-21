from .base_gsx_serializer import BaseGSXSerializer
from rest_framework import serializers
from gsx.core import GSXRequest
import copy

class AcknowledgeDeliverySerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    data = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "consignment",
            "delivery/acknowledge",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
