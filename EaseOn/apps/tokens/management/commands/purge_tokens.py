# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from tokens.models import Token


class Command(BaseCommand):
    help = 'Purge all exiting tokens.'

    def handle(self, *args, **options):
        try:
            Token.all_objects.all().hard_delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully Purged all the tokens.')
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR('Could not deleted all the tokens')
            )
            raise e
