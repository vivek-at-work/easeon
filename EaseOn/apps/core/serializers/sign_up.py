# -*- coding: utf-8 -*-
import time

from core.gsx import GSXRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

USER_MODEL = get_user_model()


class SignUpSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        """
        Check that gsx_auth_token from gsx if it is valid and via token refresh.
        """
        if settings.VALIDATE_GSX_AUTH_TOKEN_ON_SIGN_UP:
            req = GSXRequest(
                'authenticate',
                'token',
                data['gsx_user_name'],
                data['gsx_auth_token'],
                data['gsx_ship_to']
            )
            result = req.post(
                userAppleId=data['gsx_user_name'],
                authToken=data['gsx_auth_token'],
            )
            if 'gsx_response' in result:
                result = result['gsx_response']
            if 'authToken' in result:
                data['gsx_auth_token'] = result['authToken']
            else:
                raise serializers.ValidationError(
                    'Could Not Validate your GSX Details from GSX.'
                )
        return data

    class Meta:
        model = USER_MODEL
        extra_kwargs = {'username': {'default': str(time.time())}}
        fields = (
            'email',
            'username',
            'first_name',
            'city',
            'pin_code',
            'last_name',
            'contact_number',
            'gsx_technician_id',
            'gsx_user_name',
            'gsx_auth_token',
            'gsx_ship_to',
        )
