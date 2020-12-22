# -*- coding: utf-8 -*-
import sys
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
USER = get_user_model()

class Command(BaseCommand):
    """
    Updates is_admin flag to true / false based on usertype
    """

    help = "Updates is_admin flag to true / false based on usertype"

    def handle(self, *args, **options):
        self.stdout.write("Checking...")
        users = USER.objects.all()
        for u in users:
            if u.user_type == 1 and not u.is_admin == True:
                u.is_admin = True
                u.save()
                sys.stdout.write("Setting is_admin true for {}".format(u))
            elif u.user_type != 1 and  u.is_admin == True:
                u.is_admin = False
                u.save()
                sys.stdout.write("Setting is_admin false for {}".format(u))
        sys.stdout.write("Sync Completed")
