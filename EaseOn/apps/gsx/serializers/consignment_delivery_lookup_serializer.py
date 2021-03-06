# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer


class ConsignmentDeliveryLookupSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    sizePerPage = serializers.IntegerField(default=10)
    pageNumber = serializers.IntegerField(default=1)
    search_criteria = serializers.JSONField()

    def create(self, validated_data):
        pageSize = self.validated_data["sizePerPage"]
        pageNumber = self.validated_data["pageNumber"]

        url = f"delivery/lookup?pageSize={pageSize}&pageNumber={pageNumber}"
        req = GSXRequest(
            "consignment",
            url,
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data["search_criteria"])
        response = req.post(**data)
        return response
