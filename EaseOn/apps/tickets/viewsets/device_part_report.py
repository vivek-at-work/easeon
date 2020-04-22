# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers


class DevicePartReportViewSet(viewsets.BaseBulkCreateViewSet):
    queryset = models.DevicePartReport.objects.all()
    serializer_class = serializers.DevicePartReportSerializer
