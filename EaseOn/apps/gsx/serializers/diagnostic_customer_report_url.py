# -*- coding: utf-8 -*-
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_serializer import BaseGSXSerializer
from .validators import validate_device_identifier


class DiagnosticsReportDownloadSerializer(BaseGSXSerializer):
    """
    DiagnosticsReportDownloadSerializer
    """

    service = 'diagnostics'
    action = ('customer-report-url',)
    eventNumber = serializers.CharField()
