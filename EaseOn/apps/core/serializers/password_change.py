# -*- coding: utf-8 -*-
from core.utils import time_by_adding_business_days
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', True
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', True
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError('Old password did not match.')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError('New Password Do not match.')
        validate_password(attrs['new_password1'])
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):

        self.set_password_form.save()
        self.user.increment_password_change_time()
        self.user.save()
        if not self.logout_on_password_change:
            update_session_auth_hash(self.request, self.user)
