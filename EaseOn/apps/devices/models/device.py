# -*- coding: utf-8 -*-
import re

from core import utils
from core.models import BaseModel
from core.utils import send_mail, time_by_adding_business_days
from devices.exceptions import DeviceDetailsExceptions
from devices.validators import (
    gsx_validate,
    validate_identifier,
    validate_restricted_device,
)
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class Device(BaseModel):
    serial_number = models.CharField(
        null=True,
        max_length=20,
        validators=[validate_identifier, validate_restricted_device],
    )
    alternate_device_id = models.CharField(
        null=True,
        max_length=20,
        validators=[validate_identifier, validate_restricted_device],
    )
    product_name = models.CharField(null=True, max_length=100)
    configuration = models.CharField(null=True, max_length=100)
    gsx_repair_type = models.CharField(null=True, max_length=100)
    gsx_service_non_repair_type = models.CharField(null=True, max_length=100)
    address_cosmetic_changes = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    def _set_device_identifier(self, number):
        if gsx_validate(number, "alternateDeviceId"):
            self.alternate_device_id = number
        else:
            self.serial_number = number

    def _get_device_identifier(self):
        if self.alternate_device_id:
            return self.alternate_device_id
        if self.serial_number:
            return self.serial_number
        return "NA"

    @property
    def identifier(self):
        return self._get_device_identifier()

    @identifier.setter
    def identifier(self, number):
        self._set_device_identifier(number)

    @property
    def is_exempted_device(self):
        return (
            self.alternate_device_id in settings.EXEMPTED_DEVICE
            or self.serial_number in settings.EXEMPTED_DEVICE
        )

    @property
    def open_tickets(self):
        Ticket = apps.get_model(utils.get_ticket_model())
        return Ticket.objects.filter(device__serial_number=self.serial_number).open()



    def __str__(self):
        return self.identifier