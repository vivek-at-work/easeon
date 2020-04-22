# -*- coding: utf-8 -*-
import argparse

from devices.models import Device
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class Command(BaseCommand):
    help = 'Check if able to retrieve warranty Info'

    def add_arguments(self, parser):
        parser.add_argument(
            'identifier', type=str, help='Device Serial Number'
        )
        parser.add_argument('email', type=str, help='User Name')

    def handle(self, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=kwargs['email'])
            device = Device()
            device.identifier = kwargs['identifier']
            device.created_by = user
            device.save()
            device.get_warranty(user.gsx_user_name, user.gsx_auth_token)
            self.stdout.write(
                self.style.SUCCESS('Successfully retrived warranty info')
            )
        except Exception:
            self.stderr.write(
                'Could not retrived warranty info status for email {} and identifier {}'.format(
                    kwargs['email'], kwargs['identifier']
                ),
                ending='',
            )
