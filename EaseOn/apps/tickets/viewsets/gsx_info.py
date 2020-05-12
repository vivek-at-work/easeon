# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers


class GSXInfoViewSet(viewsets.BaseViewSet):
    queryset = models.GSXInfo.objects
    serializer_class = serializers.GSXInfoSerializer
