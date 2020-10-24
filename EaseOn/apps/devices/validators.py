import re
from core import utils
from devices.restricted_devices import restricted_identifiers
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.apps import apps
from django.conf import settings


def gsx_validate(value, what=None):
    """
    Tries to guess the meaning of value or validate that
    value looks like what it's supposed to be.

    >>> validate('XD368Z/A', 'partNumber')
    True
    >>> validate('XGWL2Z/A', 'partNumber')
    True
    >>> validate('ZM661-5883', 'partNumber')
    True
    >>> validate('661-01234', 'partNumber')
    True
    >>> validate('B661-6909', 'partNumber')
    True
    >>> validate('G143111400', 'dispatchId')
    True
    >>> validate('R164323085', 'dispatchId')
    True
    >>> validate('blaa', 'serialNumber')
    False
    >>> validate('MacBook Pro (Retina, Mid 2012)', 'productName')
    True
    """
    result = None

    if not isinstance(value, str):
        raise ValueError(
            '%s is not valid input (%s != string)' % (value, type(value))
        )

    rex = {
        'partNumber': r'^([A-Z]{1,4})?\d{1,3}\-?(\d{1,5}|[A-Z]{1,2})(/[A-Z])?$',
        'serialNumber': r'^[A-Z0-9]{11,12}$',
        'eeeCode': r'^[A-Z0-9]{3,4}$',
        'returnOrder': r'^7\d{9}$',
        'repairNumber': r'^\d{12}$',
        'dispatchId': r'^[A-Z]+\d{9,15}$',
        'alternateDeviceId': r'^\d{15}$',
        'diagnosticEventNumber': r'^\d{23}$',
        'productName': r'^i?Mac',
    }

    for k, v in rex.items():
        if re.match(v, value):
            result = k

    return (result == what) if what else result


def validate_identifier(value):

    """
    Check that device identifier is valid.
    """
    is_valid_alternate_device_id = gsx_validate(value, 'alternateDeviceId')
    is_valid_sn = gsx_validate(value, 'serialNumber')
    if not is_valid_alternate_device_id and not is_valid_sn:
        raise ValidationError('Not a valid serial number or IMEI number.')


def validate_open_tickets(value):
    Ticket = apps.get_model(utils.get_ticket_model())
    if value not in settings.EXEMPTED_DEVICE:
        open_tickets = (
            Ticket.objects.filter(
                Q(device__serial_number=value)
                | Q(device__alternate_device_id=value)
            )
            .open()
            .values_list('reference_number', flat=True)
        )
        if open_tickets:
            raise ValidationError(
                """This Device has pending open tickets.Close them before proceeding for a new one {0}""".format(
                    ','.join(open_tickets)
                )
            )


def validate_restricted_device(value):
    if value in restricted_identifiers:
        raise serializers.ValidationError(
            "Kindly \
         immediatly contact with administrator before proceed the repair of device."
        )
