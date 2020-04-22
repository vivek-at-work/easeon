# -*- coding: utf-8 -*-
from customers.models import Customer
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tickets.models import Ticket


class Command(BaseCommand):
    help = 'Delete All Cutomers those not have a ticket'

    def handle(self, *args, **kwargs):
        try:
            results = Customer.all_objects.exclude(
                id__in=Ticket.all_objects.all().values_list(
                    'customer', flat=True
                )
            )
            count = results.count()
            self.stdout.write(
                '{} orphan customer records found'.format(count), ending='\n'
            )
            results.hard_delete()
            self.stdout.write(
                '{} orphan customer records have been deleted'.format(count),
                ending='\n',
            )

        except Exception:
            self.stderr.write(
                'Could not perform orphan customer records deletion',
                ending='\n',
            )
