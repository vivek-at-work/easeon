from .base_gsx_serializer import BaseGSXSerializer
from core.utils import time_by_adding_business_days
from .gsx_validate import gsx_validate
from rest_framework import serializers
from gsx.core import GSXRequest
import copy


class RepairDetailsSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    repairId = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            "repair",
            "details",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data)
        response = req.get(**data)
        return response

