# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .ticket import Ticket


class Delivery(BaseModel):
    """A Service Delivery"""

    ticket = models.OneToOneField(
        Ticket, related_name="delivery", on_delete=models.CASCADE
    )
    actual_service_cost = models.FloatField(default=0.0)
    actual_hardware_cost = models.FloatField(default=0.0)
    device_pickup_time = models.DateTimeField(blank=True, null=True)
    actual_issue = models.CharField(max_length=1000)
    action_taken = models.CharField(max_length=1000)
    final_operating_system = models.CharField(max_length=50)
    outward_condition = models.CharField(max_length=1000)
    customer_signature = models.ImageField(
        upload_to="customer_signatures/deliveries", null=True, blank=True
    )

    unit_part_reports = JSONField(null=True)
    customer_feedback = JSONField(null=True)

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        ordering = ["-id"]

    def __unicode__(self):
        return self.ticket
