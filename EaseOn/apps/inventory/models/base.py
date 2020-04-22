# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models


class InventoryItem(BaseModel):
    serial_number = models.CharField(max_length=20)
    po_number = models.CharField(max_length=50)
    awb_number = models.CharField(max_length=50)
    part_number = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    consumed = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.serial_number

    class Meta:
        abstract = True
