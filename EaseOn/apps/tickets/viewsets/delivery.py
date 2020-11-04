# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
from core import viewsets
from tickets import models, serializers
from tickets.permissions import DeliveryUpdateOrDelete


class DeliveryViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.DeliverySerializer
    permission_classes = [DeliveryUpdateOrDelete]

    def get_queryset(self):
        return models.Delivery.objects.all()
