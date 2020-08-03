# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class RunDiagnosticsSerializer(BaseGSXSerializer):
    """
    RunDiagnosticsSerializer
    """

    service = 'diagnostics'
    action = 'initiate-test'
    identifier = serializers.CharField(validators=[validate_device_identifier])
    suiteId = serializers.CharField()
