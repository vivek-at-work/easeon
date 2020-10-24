# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .serializable_inventory_item import SerializableInventoryItem
from .serializable_inventory_stats import SerializableInventoryStats


@receiver(pre_save, sender=SerializableInventoryItem)
def assign_available_quantity(sender, instance, *args, **kwargs):
    stat, created = SerializableInventoryStats.objects.get_or_create(
        organization=instance.organization,
        description=instance.description,
    )
