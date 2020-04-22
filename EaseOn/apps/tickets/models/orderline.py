# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from inventory.models import RepairInventoryItem, SerializableInventoryItem

from .ticket import Ticket


class OrderLine(BaseModel):
    """A OrderLine"""

    ticket = models.ForeignKey(
        Ticket, related_name='order_lines', on_delete=models.CASCADE
    )
    kbb_serial_number = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    amount = models.FloatField(default=0.0)
    inventory_item = models.ForeignKey(
        RepairInventoryItem,
        related_name='order_line',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Replacement Spare'
        verbose_name_plural = 'Replacement Spares'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['inventory_item']
        else:
            return []

    def __str__(self):
        return '{0}'.format(self.kgb_serial_number)


@receiver(post_save, sender=OrderLine)
def disable_inventory_item(sender, instance, created, **kwargs):
    if created:
        inventory_item = instance.inventory_item
        inventory_item.consumed = True
        inventory_item.save()
    elif instance.is_deleted:
        inventory_item = instance.inventory_item
        inventory_item.consumed = False
        inventory_item.save()


# @receiver(post_delete, sender=OrderLine)
# def enable_inventory_item(sender, instance, *args, **kwargs):
#     inventory_item = instance.inventory_item
#     inventory_item.consumed = False
#     inventory_item.save()


class SerializableOrderLine(BaseModel):
    """A OrderLine"""

    ticket = models.ForeignKey(
        Ticket,
        related_name='serializable_order_lines',
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    amount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Serializable Replacement Spare'
        verbose_name_plural = 'Serializable Replacement Spares'

    def __str__(self):
        return '{0}'.format(self.description)


@receiver(post_save, sender=SerializableOrderLine)
def reduce_inventory_item(sender, instance, created, **kwargs):
    if created:
        description = instance.description
        quantity = instance.quantity
        organization = instance.ticket.organization
        entries = SerializableInventoryItem.objects.filter(
            description=description,
            organization=organization,
            available_quantity__gt=0,
        )
        consumed = 0
        for e in entries:
            pending = quantity - consumed
            if pending > 0:
                if e.available_quantity >= pending:
                    consumed = consumed + pending
                    e.consumed_quantity = e.consumed_quantity + pending
                    e.available_quantity = e.available_quantity - pending
                    pending = 0
                    e.save()
                elif e.available_quantity < pending:
                    consumed = consumed + e.available_quantity
                    pending = pending - e.available_quantity
                    s = e.consumed_quantity + e.available_quantity
                    e.consumed_quantity = s
                    e.available_quantity = 0
                    e.save()
    elif instance.is_deleted:
        description = instance.description
        quantity = instance.quantity
        organization = instance.ticket.organization

        SerializableInventoryItem.objects.create(
            organization=organization,
            description=description,
            quantity=quantity,
            available_quantity=quantity,
            consumed_quantity=0,
            created_by=get_user_model().objects.first(),
        )


@receiver(post_delete, sender=SerializableOrderLine)
def add_inventory_item(sender, instance, *args, **kwargs):
    description = instance.description
    quantity = instance.quantity
    organization = instance.ticket.organization

    SerializableInventoryItem.objects.create(
        organization=organization,
        description=description,
        quantity=quantity,
        available_quantity=quantity,
        consumed_quantity=0,
        created_by=get_user_model().objects.first(),
    )
