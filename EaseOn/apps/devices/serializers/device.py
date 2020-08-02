# -*- coding: utf-8 -*-
from core import utils
from core.serializers import BaseMeta, BaseSerializer
from devices.models import Device
from devices.validators import (validate_identifier, validate_open_tickets,
                                validate_restricted_device)
from rest_framework import serializers


class DeviceSerializer(BaseSerializer):
    identifier = serializers.CharField(
        required=True,
        validators=[
            validate_identifier,
            validate_open_tickets,
            validate_restricted_device,
        ],
    )

    def __init__(self, *args, **kwargs):
        super(DeviceSerializer, self).__init__(*args, **kwargs)
        if 'view' in self.context:
            action = self.context['view'].action
            if action == 'update':
                self.fields['identifier'] = serializers.CharField(
                    required=True,
                    validators=[
                        validate_identifier,
                        validate_restricted_device,
                    ],
                )

    class Meta(BaseMeta):
        model = Device
        fields = [
            'url',
            'product_name',
            'configuration',
            'identifier',
            'serial_number',
            'alternate_device_id',
        ]
