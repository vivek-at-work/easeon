# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from gsx.core import GSXRequest
from rest_framework import serializers

USER = get_user_model()


class BaseGSXSerializer(serializers.Serializer):
    service = ''
    action = ''
    http_verb = 'POST'

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

    def get_payload(self, validated_data):
        payload = {}
        if 'identifier' in validated_data:
            payload['device'] = {'id': validated_data['identifier']}
        for key in validated_data.keys():
            if key != 'id':
                payload[key] = validated_data[key]
        return payload

    def create(self, validated_data):
        """
        :param validated_data: valid data
        """
        req = GSXRequest(
            self.service,
            self.action,
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        if self.http_verb.upper() == 'POST':
            return req.post(**self.get_payload(validated_data))
        else:
            return req.get(**self.get_payload(validated_data))
