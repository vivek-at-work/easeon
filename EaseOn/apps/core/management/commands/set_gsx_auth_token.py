# -*- coding: utf-8 -*-
import sys

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
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

    help = "set gsx auth token for user"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("token", type=str)

    def handle(self, *args, **options):
        user = USER.objects.get(email=options["email"])
        user.gsx_auth_token = options["token"]
        user.refresh_gsx_token()
        user.save()
