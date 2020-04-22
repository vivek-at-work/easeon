# -*- coding: utf-8 -*-
from SLAs import models


def get_default_ticket_sla():
    return models.SLAs.objects.get_default_ticket_sla()


def get_default_delivery_sla():
    return models.SLAs.objects.get_default_delivery_sla()
