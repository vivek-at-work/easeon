# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from lists.models import Item


class Command(BaseCommand):
    help = "Deletes all Lists Items"

    def handle(self, *args, **options):
        try:
            Item.all_objects.all().hard_delete()
            self.stdout.write(self.style.SUCCESS("Successfully deleted all the Lists."))
        except Exception as e:
            self.stderr.write(self.style.ERROR("Could not deleted all the Lists"))
            raise e
