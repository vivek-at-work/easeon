from .base_gsx_serializer import BaseGSXSerializer
from rest_framework import serializers
from gsx.core import GSXRequest



class ContentArticleSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    articleId = serializers.CharField()

    def create(self, validated_data):
        req = GSXRequest(
            "content",
            "article",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )

        response = req.get(**self.validated_data)
        return response

