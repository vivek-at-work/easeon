from .base_gsx_serializer import BaseGSXSerializer
from core.utils import time_by_adding_business_days
from .gsx_validate import gsx_validate
from rest_framework import serializers
from gsx.core import GSXRequest
import copy

class DocumentDownloadSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    search_criteria = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "document-download",
            "",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["search_criteria"]})
        response = req.post(**data)
        return response

