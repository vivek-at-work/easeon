# -*- coding: utf-8 -*-
from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """
    Serializer for Token model.
    """

    uuid = serializers.CharField()
    message = serializers.CharField()
    token = serializers.CharField()
    url = serializers.CharField()
