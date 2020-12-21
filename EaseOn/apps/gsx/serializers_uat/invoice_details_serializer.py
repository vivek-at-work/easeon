from .base_gsx_serializer import BaseGSXSerializerUAT
from rest_framework import serializers
from gsx.core import GSXRequestUAT
import copy

class InvoiceDetailsSerializer(BaseGSXSerializerUAT):
    """
    DeviceSerializer
    """

    invoiceId  = serializers.CharField(default="123444")

    def create(self, validated_data):
        req = GSXRequestUAT(
            "invoice",
            "details",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        data = copy.deepcopy({'invoiceId':self.validated_data['invoiceId']})
        response = req.get(**data)
        return response
