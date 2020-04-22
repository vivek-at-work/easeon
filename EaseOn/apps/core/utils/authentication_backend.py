# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

logger = logging.getLogger('easeOn')


class EaseOnAuthenticationBackend(ModelBackend):
    """
    Custom Authentication Backend to validate user against
    email and password
    """

    def authenticate(self, request, **kwargs):
        try:
            user_model = get_user_model()
            email = kwargs.get('email')
            if not email:
                email = kwargs.get('username')
            if email:
                logging.info(
                    'Login Request received for email {0}'.format(email)
                )
                user = user_model.objects.get(email=email)
                logging.info('Existing user found for email {0}'.format(email))
            else:
                return None
        except user_model.DoesNotExist:
            logging.error(
                'Existing user not found for email {0}'.format(email)
            )
            return None
        else:
            password = kwargs['password']
            if user.check_password(password):
                logging.info(
                    'Password check succeeded for email {0}'.format(email)
                )
                return user
            logging.error('Password check failed for email {0}'.format(email))
