# -*- coding: utf-8 -*-
from django.db import models
from organizations.models import Organization


class NonSerializedInventoryStats(models.Model):
    organization = models.ForeignKey(
        Organization,
        related_name='non_serialized_inventory_stats',
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=100)
    total_quantity = models.IntegerField(default=0)
    total_available_quantity = models.IntegerField(default=0)
    total_consumed_quantity = models.IntegerField(default=0)
