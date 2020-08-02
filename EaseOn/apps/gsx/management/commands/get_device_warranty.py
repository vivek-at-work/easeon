# -*- coding: utf-8 -*-
import sys

from core.utils import time_by_adding_business_days
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import ProjectState
from django.db.utils import OperationalError
from gsx.core import GSXRequest

USER = get_user_model()


class Command(BaseCommand):
    """
    Detect if any apps have missing migration files
    (not necessarily applied though)
    Based on: https://gist.github.com/nealtodd/a8f87b0d95e73eb482c5
    """

    help = 'set gsx auth token for user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str)
        parser.add_argument('--device', type=str, default='FCGT24E5HFM2')

    def _get_device_warranty(self, user, device):
        req = GSXRequest(
            'repair',
            'product/details?activationDetails=true',
            user.gsx_user_name,
            user.gsx_auth_token,
            user.gsx_ship_to,
        )
        device = {'id': device}
        received_on = time_by_adding_business_days(0).isoformat()
        response = req.post(unitReceivedDateTime=received_on, device=device)
        print(response)

    def handle(self, *args, **options):
        if 'email' in options and options['email'] is not None:
            user = USER.objects.get(email=options['email'])
            self._get_device_warranty(user, options['device'])
        else:
            users = USER.objects.all()
            for user in users:
                self._get_device_warranty(user, options['device'])
