# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from tickets import models, serializers


class GSXInfoViewSet(viewsets.BaseViewSet):
    queryset = models.GSXInfo.objects
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    serializer_class = serializers.GSXInfoSerializer
