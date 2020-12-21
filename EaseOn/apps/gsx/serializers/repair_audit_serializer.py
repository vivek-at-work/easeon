from .base_gsx_serializer import BaseGSXSerializer
from rest_framework import serializers
from gsx.core import GSXRequest
import copy

class RepairAuditSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    repairId = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            "repair", "audit", self.gsx_user_name,
             self.gsx_auth_token, self.gsx_ship_to
        )
        data = copy.deepcopy(self.validated_data)
        response = req.get(**data)
        return response

