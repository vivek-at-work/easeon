# -*- coding: utf-8 -*-
from core.viewsets import BaseViewSet

from reporting import models, serializers


class ReportsViewSet(BaseViewSet):
    queryset = models.ReportRequest.objects
    serializer_class = serializers.ReportRequestSerializer
