# -*- coding: utf-8 -*-
import sys

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connections
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import ProjectState
from django.db.utils import OperationalError

USER = get_user_model()


class Command(BaseCommand):
    """
    Detect if any apps have missing migration files
    (not necessarily applied though)
    Based on: https://gist.github.com/nealtodd/a8f87b0d95e73eb482c5
    """

    help = 'set gsx auth token for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email', type=str,
        )

    def refresh_gsx_token(self, user):
        gsx_user_name = user.gsx_user_name
        gsx_auth_token = user.gsx_auth_token
        gsx_ship_to = user.gsx_ship_to
        refresh_status = user.refresh_gsx_token()
        if refresh_status:
            print('GSX Login Success for user', gsx_user_name)
        else:
            print(
                f'GSX Login Filed for user {gsx_user_name} with shipto {gsx_ship_to} and token {gsx_auth_token}'
            )

    def handle(self, *args, **options):
        if 'email' in options and options['email'] is not None:
            user = USER.objects.get(email=options['email'])
            self.refresh_gsx_token(user)
        else:
            users = USER.objects.all()
            for user in users:
                self.refresh_gsx_token(user)
