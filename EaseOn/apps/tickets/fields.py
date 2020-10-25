# -*- coding: utf-8 -*-
from inventory.models import RepairInventoryItem
from inventory.serializers import RepairItemSerializer
from rest_framework import serializers


class RepairInventoryItemField(serializers.Field):
    def to_representation(self, obj):
        return RepairItemSerializer(obj, context=self.context).data

    def to_internal_value(self, data):
        if isinstance(data, int):
            return RepairInventoryItem.objects.get(pk=data)
        else:
            return RepairInventoryItem.objects.get(pk=int(data["id"]))
