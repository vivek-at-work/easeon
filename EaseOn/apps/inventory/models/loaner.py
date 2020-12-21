# -*- coding: utf-8 -*-
from core.models import BaseManager, BaseModel, BaseQuerySet
from django.db import models
from organizations.models import Organization

from .base import InventoryItem


class LoanerInventoryManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super(LoanerInventoryManager, self).__init__(*args, **kwargs)
        self.alive_only = True

    def get_queryset(self):
        return LoanerInventoryQuerySet(self.model).filter(is_deleted=False)


class LoanerInventoryQuerySet(BaseQuerySet):
    def available(self):
        return self.filter(consumed=False, blocked=False)


class LoanerItemPenaltyAmount(BaseModel):
    part_number = models.CharField(max_length=20)
    reason = models.CharField(max_length=100)
    cost = models.FloatField(default=0.0)
    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)


class LoanerInventoryItem(InventoryItem):
    organization = models.ForeignKey(
        Organization, related_name="loaner_inventory_items", on_delete=models.CASCADE
    )
    objects = LoanerInventoryManager()
    all_objects = LoanerInventoryManager(alive_only=False)

    class Meta:
        verbose_name = "Loaner Inventory Item"
        verbose_name_plural = "Loaner Inventory Items"
        ordering = ["-created_at"]

    @property
    def penalty(self):
        """ Get Penalty """
        results = []
        for item in LoanerItemPenaltyAmount.objects.filter(
            part_number=self.part_number
        ):
            results.append({"reason": item.reason, "cost": item.cost})
        return results

    def __str__(self):
        return self.serial_number
