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

    def _authenticate(self, email, password):
        return authenticate(
            self.context.get('request'),
            **{'email': email, 'password': password}
        )

    def validate(self, attrs):
        failed_login_msz = 'Could not Validate User with provided credentials.'
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user_by_email = (
                get_user_model()
                .objects.filter(email__iexact=email, is_active=True)
                .exists()
            )
            if not user_by_email:
                raise exceptions.ValidationError('User does not exists.')
            else:
                user = self._authenticate(email, password)
                if user:
                    attrs['user'] = user
                    return attrs
                else:
                    raise exceptions.ValidationError(failed_login_msz)
        else:
            msg = 'Insufficient Login information provided.'
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
