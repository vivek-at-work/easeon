# -*- coding: utf-8 -*-
import argparse
import logging

from devices.models import Device
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Delete All Devices those not have a ticket"

    def handle(self, *args, **kwargs):
        try:
            results = Device.all_objects.exclude(
                id__in=Ticket.all_objects.all().values_list("device", flat=True)
            )
            count = results.count()
            logging.info(f"{count} Orphan device records found.")
            results.hard_delete()
            logging.info(f"{count} Orphan device records have been deleted.")

        except Exception:
            logging.error("Could not perform Orphan device records deletion.")
