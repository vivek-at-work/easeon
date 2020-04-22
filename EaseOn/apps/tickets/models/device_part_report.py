# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from lists import models as list_models

from .ticket import Ticket


class DevicePartReport(BaseModel):
    """Unit Part Condition"""

    part = models.CharField(max_length=50)
    initial_status = models.CharField(max_length=50, default="Didn't Check")
    final_status = models.CharField(max_length=50, default="Didn't Check")
    ticket = models.ForeignKey(
        Ticket, related_name='device_part_reports', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Device Part Report'
        verbose_name_plural = 'Device Part Reports'

    def __unicode__(self):
        return self.part

    @staticmethod
    def get_initial_device_part_report():
        reports = []
        for i in list_models.Item.objects.filter(list_name='UNIT_PART'):
            reports.append({'part': i.value, 'initial_status': "Did't Check"})
        return reports
