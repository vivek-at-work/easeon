# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import authenticate, get_user_model
from django.urls import reverse
from rest_framework import exceptions, serializers

USER_MODEL = get_user_model()


class OTPOptionsSerializer(serializers.Serializer):
    """
    OTPOptionsSerializer used to show OTP options for User
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def _authenticate_via_email(self, email, password):
        user = None
        if email and password:
            user = authenticate(
                self.context.get('request'),
                **{'email': email, 'password': password}
            )
            if not user:
                raise Exception()
            return user
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            unauthenticated_user = get_user_model().objects.get(
                email__iexact=email
            )
            if not unauthenticated_user.is_active:
                msg = 'User account has been disabled.'
                raise exceptions.ValidationError(msg)
            user = self._authenticate_via_email(email, password)
            attrs['user'] = user
            return attrs
        except Exception:
            msg = 'Unable to login with provided credentials.'
            raise exceptions.ValidationError(msg)

    def to_representation(self, data):
        user = data['user']
        return {
            'email': user.email,
            'otp_receive_options': user.contact_number.split(',')
            + [user.email],
            'message': self._get_message(),
        }

    def _get_message(self):
        return 'Select the contact number you wish to receive OTP On.'
