# -*- coding: utf-8 -*-
import logging

from customers.models import Customer
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from lists.models import Item
from reporting.db_query import REPORT_SQL_MAPPING


class Command(BaseCommand):
    help = 'Sync Report Types'

    def handle(self, *args, **kwargs):
        for k in REPORT_SQL_MAPPING:
            Item.objects.get_or_create(
                list_name='REPORT_TYPES',
                value=k,
                created_by=get_user_model().objects.first(),
            )
