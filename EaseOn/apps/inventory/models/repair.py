# -*- coding: utf-8 -*-
from core.models import BaseManager, BaseQuerySet
from django.db import models
from organizations.models import Organization

from .base import InventoryItem


class RepairInventoryManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super(RepairInventoryManager, self).__init__(*args, **kwargs)
        self.alive_only = True

    def get_queryset(self):
        return RepairInventoryQuerySet(self.model).filter(is_deleted=False)


class RepairInventoryQuerySet(BaseQuerySet):
    def available(self):
        return self.filter(consumed=False, blocked=False)


class RepairInventoryItem(InventoryItem):
    organization = models.ForeignKey(
        Organization, related_name="repair_inventory_items", on_delete=models.CASCADE
    )
    consignment_type = models.CharField(max_length=20)
    objects = RepairInventoryManager()
    all_objects = RepairInventoryManager(alive_only=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.serial_number
