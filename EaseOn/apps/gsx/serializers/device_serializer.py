# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from core.utils import time_by_adding_business_days
from django.contrib.auth import get_user_model
from gsx.core import GSXRequest
from .base_serializer import BaseGSXSerializer
from rest_framework import serializers
from .validators import validate_device_identifier


class DeviceSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField(validators=[validate_device_identifier])

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
