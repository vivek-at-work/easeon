# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from tickets import models, serializers


class DeliveryViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.DeliverySerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]

    def get_queryset(self):
        return models.Delivery.objects.all()
