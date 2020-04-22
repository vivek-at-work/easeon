# -*- coding: utf-8 -*-
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    SerializableInventoryItemSerializer,
    SerializableInventoryListSerializer,
)


class SerializableItemViewSet(BaseBulkCreateViewSet):
    serializer_class = SerializableInventoryItemSerializer
    list_serializer_class = SerializableInventoryListSerializer
    delete_serializer_class = SerializableInventoryListSerializer
    ordering = ['id']

    def get_queryset(self):
        return models.SerializableInventoryItem.objects.all()
