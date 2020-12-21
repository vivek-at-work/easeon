from .base_gsx_serializer import BaseGSXSerializer
from rest_framework import serializers
from gsx.core import GSXRequest
import copy

class AttachmentUploadAccessSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    data = serializers.JSONField()

    def create(self, validated_data):
        req = GSXRequest(
            "attachment",
            "upload-access",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        response_headers, message = req.post(
            **self.validated_data["data"], return_headers=True
        )
        headers = dict(response_headers)
        cid = headers.get("X-Apple-Gigafiles-Cid", None)
        token = headers.get("X-Apple-AppToken", None)
        message.update({"X-Apple-Gigafiles-Cid": cid, "X-Apple-AppToken": token})
        return message
