# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from core.utils import time_by_adding_business_days
from gsx.core import GSXRequest
from django.contrib.auth import get_user_model
import re
USER = get_user_model()

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


class BaseGSXSerializer(serializers.Serializer):
    @property
    def gsx_user_name(self):
        return self.user.gsx_user_name

    @property
    def gsx_auth_token(self):
        return self.user.gsx_auth_token

    @property
    def gsx_ship_to(self):
        return self.user.gsx_ship_to

    @property
    def user(self):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user
        else:
            return USER.objects.get(email='kuldeep.rawat@unicornstore.in')



class DeviceSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
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
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        received_on = time_by_adding_business_days(0).isoformat()
        response = req.post(unitReceivedDateTime=received_on, device=device)
        return response


class DiagnosticSuitesSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
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
        req = GSXRequest(
            'diagnostics',
            'suites',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        response = req.get(deviceId=validated_data['identifier'])
        return response


class RepairEligibilitySerializer(BaseGSXSerializer):
    """
    DeviceSerializer
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
        req = GSXRequest(
            'repair',
            'eligibility',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        response = req.post(device=device)
        return response


class DiagnosticsLookupSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
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
        req = GSXRequest(
            'diagnostics',
            'lookup',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        response = req.post(device=device)
        return response


class RunDiagnosticsSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField()
    suiteId = serializers.CharField()

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
        req = GSXRequest(
            'diagnostics',
            'initiate-test',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        diagnostics = {'suiteId': validated_data['suiteId']}
        response = req.post(device=device, diagnostics=diagnostics,)
        return response


class DiagnosticsStatusSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
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
        req = GSXRequest(
            'diagnostics',
            'status',
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {'id': validated_data['identifier']}
        response = req.post(device=device)
        return response
