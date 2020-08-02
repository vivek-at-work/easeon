# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

import logging

from core.serializers import OTPOptionsSerializer
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from oauth2_provider.models import (get_access_token_model,
                                    get_application_model,
                                    get_refresh_token_model)
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.mixins import OAuthLibMixin
from otp.models import PyOTP
from otp.serializers import HotpSerializer, VerifyOtpSerializer
from rest_framework import permissions
from rest_framework import status as rest_status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token as TokenModel
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rocketchat.rocketchat import RocketChat

USER = get_user_model()


class LoginViewSet(OAuthLibMixin, viewsets.GenericViewSet):
    """OTP Viewset, every OTP http request handles by this class

    """

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
    lookup_field = 'email'
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'get_otp_options':
            return OTPOptionsSerializer
        elif self.action == 'generate_otp':
            return HotpSerializer
        elif self.action == 'verify_otp':
            return VerifyOtpSerializer

    def _get_user_url(self, user, request):
        return reverse('user-detail', kwargs={'pk': user.id}, request=request,)

    def _validate(self, serializer, data):
        """
        :param serializer: serializer against which data to ve validated
        :param data: data to ve validated
        :return: serializer instance.
        """

        serializer_instance = serializer(data=data)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()

    def get_otp_options(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer_instance = serializer(data=request.data)
        serializer_instance.is_valid(raise_exception=True)
        data = serializer_instance.data
        return Response(data, status=rest_status.HTTP_201_CREATED)

    def generate_otp(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return Response(serializer, status=rest_status.HTTP_201_CREATED)

    def verify_otp(self, request, uuid):
        """

        :param request: Django request
        :param otp_type: otp_type  [hotp/totp]
        :param uuid: OTP instance UUID
        :return: 200_ok OR 400_bad_request
        """
        otp_type = 'hotp'
        obj = PyOTP.objects.get(uuid=uuid)
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_otp = serializer.verify_otp(
            serializer.data.get('otp'), obj, otp_type
        )
        FH = rest_status.HTTP_400_BAD_REQUEST
        if not valid_otp:
            logging.warning(
                'OTP validation failed for user {}'.format(request.user)
            )
            return Response(status=FH)
        logging.info(
            'OTP validation succeeded for user {}'.format(request.user)
        )

        url, headers, body, status = self.create_token_response(request)
        user = None
        response = None
        if status == 200:
            import json

            access_token = json.loads(body).get('access_token')
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token
                )
                user = token.user
                app_authorized.send(sender=self, request=request, token=token)
                chat_login = {}
                if settings.ENABLE_CHAT:
                    chat_login = self.create_chat_login(
                        user.email,
                        serializer.data.get('password'),
                        user.full_name,
                    )
                if user:
                    res = {}
                    res['auth'] = json.loads(body)
                    res['user'] = {}
                    res['user']['full_name'] = user.full_name
                    res['user']['url'] = self._get_user_url(user, request)
                    res['user'][
                        'need_to_change_password'
                    ] = user.need_to_change_password
                    res['user']['is_superuser'] = user.is_superuser
                    res['user']['role'] = user.role
                    res['chat_login'] = chat_login
                    response = HttpResponse(
                        content=json.dumps(res), status=status
                    )
                else:
                    response = HttpResponse(content=body, status=status)
            for k, v in headers.items():
                response[k] = v
        else:
            raise NotAuthenticated(detail='Unable To Login', code=status)
        return response

    def refresh_token(self, request):
        url, headers, body, status = self.create_token_response(request)
        user = None
        response = None
        if status == 200:
            import json

            access_token = json.loads(body).get('access_token')
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token
                )
                user = token.user
                app_authorized.send(sender=self, request=request, token=token)
                if user:
                    res = {}
                    res['auth'] = json.loads(body)
                    res['user'] = {}
                    res['user']['full_name'] = user.full_name
                    res['user']['url'] = self._get_user_url(user, request)
                    res['user'][
                        'need_to_change_password'
                    ] = user.need_to_change_password
                    res['user']['is_superuser'] = user.is_superuser
                    response = HttpResponse(
                        content=json.dumps(res), status=status
                    )
                else:
                    response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    def create_chat_login(self, email, password, name):
        username = email.replace('@', '-')
        if email == 'admin@easeon.in':
            return RocketChat().users_create_token(username='admin').json()
        userQuery = RocketChat().users_info(username=username).json()
        if userQuery['success']:
            RocketChat(username, password).users_create_token(
                username=username
            ).json()
        else:
            cretion_repsone = (
                RocketChat()
                .users_create(
                    email=email,
                    name=name,
                    password=password,
                    username=username,
                )
                .json()
            )
            print(cretion_repsone)
        return (
            RocketChat(username, password)
            .users_create_token(username=username)
            .json()
        )
