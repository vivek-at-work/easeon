# -*- coding: utf-8 -*-
import copy
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class BaseGSXSerializerUAT(serializers.Serializer):
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
        return USER.objects.get(email="unicorn_tech_aprvlnotreqrd@unicorn.com")
