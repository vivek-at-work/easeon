# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


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
