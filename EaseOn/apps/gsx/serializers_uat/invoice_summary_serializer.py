# -*- coding: utf-8 -*-
import copy

from gsx.core import GSXRequestUAT
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializerUAT


def get_dummay_payload():  # This is a callable
    # return {"shipTo": "0001026647"}
    return {
        "createdToDate": "2020-12-03T12:31:18.050Z",
        "createdFromDate": "2020-11-20T12:31:18.051Z",
    }


class InvoiceSummarySeralizer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    data = serializers.JSONField(default=get_dummay_payload)

    def create(self, validated_data):
        req = GSXRequestUAT(
            "invoice",
            "summary",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({"payload": self.validated_data["data"]})
        response = req.post(**data)
        return response
