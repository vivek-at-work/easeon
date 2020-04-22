# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from organizations.models import Organization


class SerializableInventoryItem(BaseModel):
    organization = models.ForeignKey(
        Organization,
        related_name='serializable_inventory_items',
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    available_quantity = models.IntegerField(default=0)
    consumed_quantity = models.IntegerField(default=0)
    consignment_type = models.CharField(max_length=20)


@receiver(pre_save, sender=SerializableInventoryItem)
def my_callback(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.available_quantity = instance.quantity
