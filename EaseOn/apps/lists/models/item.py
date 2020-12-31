# -*- coding: utf-8 -*-
from collections import defaultdict

from core.models import BaseModel
from django.db import models

LIST_NAME_CHOICES = (
    ("TICKET_STATUS", "Ticket Status"),
    ("COVERAGE_TYPE", "Coverage Type"),
    ("GSX_SERVICE_TYPE", "GSX Service Type"),
    ("REPAIR_TYPE", "Repair Type"),
    ("GSX_REPAIR_TYPE", "GSX Repair Type"),
    ("CUSTOMER_TYPE", "Customer Type"),
    ("UNIT_PART", "Unit Part"),
    ("STATES", "States"),
    ("COUNTRY", "COUNTRY"),
    ("SERIALIZABLE_INVENTORY_ITEM", "Serializable Inventory Item"),
    ("LOANER_INVENTORY_PART_NUMBERS", "Loaner Inventory Part Numbers"),
    ("LOANER_INVENTORY_PENALTY_REASONS", "Loaner Inventory Penalty Reasons"),
    ("CONSIGNMENT_TYPE", "Consignment Types"),
    ("REPORT_TYPES", "Report Types")
   )


class Item(BaseModel):
    value = models.CharField(max_length=100)
    list_name = models.CharField(
        max_length=100, choices=LIST_NAME_CHOICES, default="TICKET_STATUS"
    )

    class Meta:
        verbose_name = "List Item"
        verbose_name_plural = "List Items"

    def __unicode__(self):
        return str(self.value)


def get_list_dict():
    result = defaultdict(list)
    for choice in LIST_NAME_CHOICES:
        key = "{0}s".format(choice[0].lower())
        result[key] = Item.objects.filter(list_name=choice[0]).values("value")
    BOOLEAN_LIST = [{"value": True}, {"value": False}]
    result["is_standby_device_required"] = BOOLEAN_LIST
    result["is_backup_required"] = BOOLEAN_LIST
    return result


def get_list_choices(list_name_key):
    try:
        return [
            x["value"]
            for x in Item.objects.filter(list_name=list_name_key).values("value")
        ]
    except Exception:
        return []
