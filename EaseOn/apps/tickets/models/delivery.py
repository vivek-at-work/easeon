# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .ticket import Ticket


class Delivery(BaseModel):
    """A Service Order"""

    ticket = models.OneToOneField(
        Ticket, related_name="delivery", on_delete=models.CASCADE
    )
    actual_service_cost = models.FloatField(default=0.0)
    actual_hardware_cost = models.FloatField(default=0.0)
    device_pickup_time = models.DateTimeField(blank=True, null=True)
    # gsx_reference_number = models.CharField(
    #    max_length=30, blank=True, null=True
    # )
    actual_issue = models.CharField(max_length=1000)
    action_taken = models.CharField(max_length=1000)
    final_operating_system = models.CharField(max_length=50)
    # gsx_repair_type = models.CharField(max_length=50)
    # comptia_code = models.CharField(max_length=50)
    outward_condition = models.CharField(max_length=1000)
    reference_number = models.CharField(max_length=50, unique=True)
    customer_signature = models.ImageField(upload_to="signatures", null=True)

    def __unicode__(self):
        return self.reference_number


@receiver(pre_save, sender=Delivery)
def set_reference_number_for_delivery(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        reference_number = instance.ticket.reference_number
        instance.reference_number = reference_number
