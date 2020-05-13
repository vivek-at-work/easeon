# -*- coding: utf-8 -*-
import datetime
import random
import string
import uuid

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token as TokenModel

from .django_exception_handler import *
from .pagination import *
from .token_generator import *
from .two_factor_client import TwoFactorIn
from .workdays import workday


def get_organization_model():
    return 'organizations.Organization'


def get_ticket_model():
    return 'tickets.Ticket'


def time_by_adding_business_days(add_days, from_date=timezone.now()):
    start_date = from_date.date()
    start_time = from_date.time()
    end_date = workday(start_date, add_days)
    return datetime.datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        start_time.hour,
        start_time.minute,
        start_time.second,
        tzinfo=pytz.UTC,
    )


def default_create_token(token_model, user):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


def send_mail(subject, message, *receivers, **kwargs):
    kwargs.update(
        {
            'SERVER_IP': settings.SERVER_IP,
            'site_name': settings.SITE_HEADER,
            'twitter_handle': settings.TWITTER_HANDLE,
            'REPLY_TO': settings.EMAIL_HOST_USER,
            'sender_full_name': 'Team ' + settings.SITE_HEADER,
        }
    )
    if message.endswith('.html'):
        html_content = render_to_string(message, kwargs)
        text = strip_tags(html_content)
        print(html_content)
    else:
        text = message
    msg = EmailMultiAlternatives(
        subject, text, settings.EMAIL_HOST_USER, receivers
    )
    if message.endswith('.html'):
        msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_otp(number, otp):
    return TwoFactorIn.send_otp(number, otp)


def get_random_string(min_char=8, max_char=12):

    allchar = string.ascii_letters + string.punctuation + string.digits
    password = ''.join(
        random.choice(allchar)
        for x in range(random.randint(min_char, max_char))
    )
    return password


def get_uuid():
    return uuid.uuid4()


def get_otp_token_model():
    return TokenModel


def get_url_for_account_approval_from_admin(uid, token):
    url = '{}/{}/{}'.format(
        settings.NEW_USER_ADMIN_APPROVE_URL, str(uid), str(token)
    )
    return url


def get_url_for_email_verification(uid, token):
    return '{}/{}/{}'.format(
        settings.NEW_USER_EMAIL_VERIFICATION_URL, str(uid), str(token)
    )


def get_url_password_reset(uid, token):
    return '{}/{}/{}'.format(settings.PASSWORD_RESET_URL, str(uid), str(token))


def payload_enricher(request):
    return {'sub': 'mysubject'}
