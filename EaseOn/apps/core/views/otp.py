#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
- otp.views
~~~~~~~~~~~

- This file contains API's for otp
"""

# future
from __future__ import unicode_literals

import logging

from core.serializers import UserSerializer
# Django
from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken, Application
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
# own app
from otp import models, serializers
# rest-framework
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token as TokenModel
from rest_framework.response import Response

# 3rd party


# local

USER = get_user_model()


class OTPViewSet(viewsets.GenericViewSet):
    """OTP Viewset, every OTP http request handles by this class

    """

    queryset = models.PyOTP.objects.all()
    lookup_field = 'uuid'
    token_model = TokenModel
    permission_classes = (permissions.AllowAny,)
    otp_type = None

    def get_serializer_class(self):
        if self.action == 'generate_hotp':
            return serializers.HotpSerializer
        elif self.action == 'generate_totp':
            return serializers.TotpSerializer
        elif self.action == 'generate_hotp_provision_uri':
            return serializers.HOTPProvisionUriSerializer
        elif self.action == 'generate_totp_provision_uri':
            return serializers.TOTPProvisionUriSerializer
        elif self.action == 'verify_otp':
            return serializers.VerifyOtpSerializer
        return serializers.NoneSerializer

    def _validate(self, serializer, data):
        """
        :param serializer: serializer against which data to ve validated
        :param data: data to ve validated
        :return: serializer instance.
        """

        serializer_instance = serializer(data=data)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()

    def generate_hotp(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)

        return Response(serializer, status=status.HTTP_201_CREATED)

    def generate_totp(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)

        return Response(serializer, status=status.HTTP_201_CREATED)

    def generate_hotp_provision_uri(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)

        return Response(serializer, status=status.HTTP_201_CREATED)

    def generate_totp_provision_uri(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)

        return Response(serializer, status=status.HTTP_201_CREATED)

    def verify_otp(self, request, otp_type, uuid):
        """

        :param request: Django request
        :param otp_type: otp_type  [hotp/totp]
        :param uuid: OTP instance UUID
        :return: 200_ok OR 400_bad_request
        """

        obj = self.get_object()
        serializer = self.get_serializer_class()

        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valid_otp = serializer.verify_otp(
            serializer.data.get('otp'), obj, otp_type
        )
        if not valid_otp:
            logging.warning(
                'OTP validation failed for user {}'.format(request.user)
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logging.info(
            'OTP validation succeeded for user {}'.format(request.user)
        )

        user = USER.objects.get(email=serializer.data.get('email'))
        response = UserSerializer(user, context={'request': request}).data
        return Response(data=response, status=status.HTTP_200_OK)
