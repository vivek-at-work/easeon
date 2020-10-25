# -*- coding: utf-8 -*-
from rest_framework import serializers
from tickets.models import UploadContent


class UploadContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadContent
        fields = ["description", "file", "upload_type"]
