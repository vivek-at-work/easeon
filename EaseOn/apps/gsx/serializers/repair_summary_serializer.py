from .base_gsx_serializer import BaseGSXSerializer


import copy
import re

from core.utils import time_by_adding_business_days
from django.contrib.auth import get_user_model
from gsx.core import GSXRequest
from rest_framework import serializers

USER = get_user_model()

from .base_gsx_serializer import BaseGSXSerializer
from core.utils import time_by_adding_business_days
from .gsx_validate import gsx_validate
from rest_framework import serializers
from gsx.core import GSXRequest
import copy

class RepairSummarySerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    page_size = serializers.IntegerField(default=10)
    page = serializers.IntegerField(default=1)
    fetchAllRepairs = serializers.BooleanField(default=False)
    search_criteria = serializers.JSONField()

    def create(self, validated_data):
        page_size = self.validated_data["page_size"]
        page = self.validated_data["page"]
        fetchAllRepairs = self.validated_data["fetchAllRepairs"]

        url = f"summary?pageSize={page_size}&pageNumber={page}"
        if fetchAllRepairs:
            url = f"summary?pageSize={page_size}&pageNumber={page}&fetchAllRepairs=true"

        req = GSXRequest(
            "repair", url, self.gsx_user_name, self.gsx_auth_token, self.gsx_ship_to
        )
        data = copy.deepcopy(self.validated_data["search_criteria"])
        response = req.post(**data)
        out = {
            'count':response['totalNumberOfRecords'],
            'current':page,
            'page_size':page_size,
            'results':response['repairs'] if 'repairs' in response else []
        }
        return out

