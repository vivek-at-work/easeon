# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .ticket import Ticket


class GSXInfo(BaseModel):
    """A Service Order"""

    ticket = models.ForeignKey(
        Ticket, related_name='gsx_informations', on_delete=models.CASCADE
    )
    gsx_reference_number = models.CharField(max_length=30)
    gsx_repair_type = models.CharField(max_length=50)
    comptia_code = models.CharField(max_length=50)

    def __unicode__(self):
        return self.gsx_reference_number
