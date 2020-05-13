# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers
from core.permissions import HasManagerRightsToUpdateOrDelete


class GSXInfoViewSet(viewsets.BaseViewSet):
    queryset = models.GSXInfo.objects
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    serializer_class = serializers.GSXInfoSerializer
