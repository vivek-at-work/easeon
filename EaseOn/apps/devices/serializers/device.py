# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from devices.models import Device
from devices.models import validate as gsx_validate
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers

class DeviceSerializer(BaseSerializer):
    class Meta(BaseMeta):
        model = Device
        fields = [
            'url',
            'product_name',
            'configuration',
            'identifier',
            'user_messages',
            'serial_number',
            'alternate_device_id'
        ]

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


