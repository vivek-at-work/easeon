# -*- coding: utf-8 -*-
import logging
from customers.models import Customer
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Delete All Cutomer Records those not have a ticket'
    def handle(self, *args, **kwargs):
        try:
            results = Customer.all_objects.exclude(
                id__in=Ticket.all_objects.all().values_list(
                    'customer', flat=True
                )
            )
            count = results.count()
            logging.info(f"{count} Orphan Customer records found.")
            results.hard_delete()
            logging.info(f"{count} Orphan customer records have been deleted")

        except Exception:
            logging.error('Could not perform orphan customer records deletion')
