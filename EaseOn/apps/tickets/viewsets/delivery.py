# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
from core import viewsets
from tickets import models, serializers


class DeliveryViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.DeliverySerializer

    def get_queryset(self):
        return models.Delivery.objects.all()
