# -*- coding: utf-8 -*-
from core.models import BaseManager, BaseModel, BaseQuerySet
from django.db import models
from organizations.models import Organization

from .base import InventoryItem


class LoanerInventoryManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super(LoanerInventoryManager, self).__init__(*args, **kwargs)
        self.alive_only = True

    def get_queryset(self):
        return LoanerInventoryQuerySet(self.model).filter(is_deleted=False)


class LoanerInventoryQuerySet(BaseQuerySet):
    def available(self):
        return self.filter(consumed=False, blocked=False)


class LoanerItemPenaltyAmount(BaseModel):
    part_number = models.CharField(max_length=20)
    reason = models.CharField(max_length=100)
    cost = models.FloatField(default=0.0)
    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)


class LoanerInventoryItem(InventoryItem):
    organization = models.ForeignKey(
        Organization, related_name="loaner_inventory_items", on_delete=models.CASCADE
    )
    objects = LoanerInventoryManager()
    all_objects = LoanerInventoryManager(alive_only=False)

    @property
    def penalty(self):
        """ Get Penalty """
        results = []
        for item in LoanerItemPenaltyAmount.objects.filter(
            part_number=self.part_number
        ):
            results.append({"reason": item.reason, "cost": item.cost})
        return results

        # if self.part_number == 'HN661-01867':
        #     return [
        #        ,
        #         {
        #             'reason': 'Exchange Price Returnable Damage',
        #             'cost': '24500',
        #         },
        #         {'reason': 'Lost Or Excessive Damage', 'cost': '35500'},
        #     ]
        # if self.part_number == 'HN661-01909':
        #     return [
        #         {'reason': 'For Display Damage Only', 'cost': '11000'},
        #         {
        #             'reason': 'Exchange Price Returnable Damage',
        #             'cost': '21000',
        #         },
        #         {'reason': 'Lost Or Excessive Damage', 'cost': '26500'},
        #     ]
        # if self.part_number == 'HN661-12386':
        #     return [
        #         {'reason': 'For Display Damage Only', 'cost': '15000'},
        #         {
        #             'reason': 'Exchange Price Returnable Damage',
        #             'cost': '30500',
        #         },
        #         {'reason': 'Lost Or Excessive Damage', 'cost': '46000'},
        #     ]
        # return [{'event': 'Damage', 'cost_price': 27000}]

    def __str__(self):
        return self.serial_number
