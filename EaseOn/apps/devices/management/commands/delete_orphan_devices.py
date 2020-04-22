# -*- coding: utf-8 -*-
import argparse

from devices.models import Device
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Delete All Devices those not have a ticket'

    def handle(self, *args, **kwargs):
        try:
            results = Device.all_objects.exclude(
                id__in=Ticket.all_objects.all().values_list(
                    'device', flat=True
                )
            )
            count = results.count()
            self.stdout.write(
                '{} orphan device records found.'.format(count), ending='\n'
            )
            results.hard_delete()
            self.stdout.write(
                '{} orphan device records have been deleted.'.format(count),
                ending='\n',
            )

        except Exception:
            self.stderr.write(
                'Could not perform orphan device records deletion.',
                ending='\n',
            )
