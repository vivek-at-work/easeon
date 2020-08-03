# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class DiagnosticsLookupSerializer(BaseGSXSerializer):
    """
    DiagnosticsLookupSerializer
    """

    service = 'diagnostics'
    action = 'lookup'
    identifier = serializers.CharField(validators=[validate_device_identifier])
