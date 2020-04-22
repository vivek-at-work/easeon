#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
- otp.serializer
~~~~~~~~~~~~~~

- This file contains pyotp app serializers
"""

# future
from __future__ import unicode_literals
from rest_framework import serializers
from core.gsx import GSXRequest
import re

class NoneSerializer(serializers.Serializer):
    pass

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


class DeviceSerializer(serializers.Serializer):
    """DeviceSerializer

    """

    identifier = serializers.CharField()

    def validate_identifier(self, value):
        """
        Check that device identifier is valid.
        """
        is_valid_alternate_device_id = gsx_validate(value, 'alternateDeviceId')
        is_valid_sn = gsx_validate(value, 'serialNumber')
        if not is_valid_alternate_device_id and not is_valid_sn:
            raise serializers.ValidationError(
                'Not a valid serial number or IMEI number.'
            )
        return value


    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        req = GSXRequest(
            'repair',
            'product/details?activationDetails=true',
            gsx_username,
            authtoken,
        )
        device = {'id': self.identifier}
        received_on = time_by_adding_business_days(0).isoformat()
        response = req.post(unitReceivedDateTime=received_on, device=device)
        if "errorId" in response:
            raise DeviceDetailsExceptions(response['errors'][0]['message'],response)
        return response

