# -*- coding: utf-8 -*-
from django.contrib.auth import tokens
from django.utils import six


class TokenGenerator(tokens.PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp)


account_activation_token = TokenGenerator()
