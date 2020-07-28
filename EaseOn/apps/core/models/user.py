# -*- coding: utf-8 -*-
import logging

from core import utils
from gsx.core import GSXRequest
from core.utils import account_activation_token
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import encoding, http, timezone
from otp.mixins import OTPMixin

from .signals import attributes_changed
from .user_manager import UserManager

SUPER_USER = 'SuperUser'
OPERATOR = 'Operator'
TOKEN_USER = 'TokenUser'
AUDITOR = 'Auditor'


def validate_user_email_domain(value):
    """
    User's email can be from particular
    set of domain names.
    """
    for domain in settings.VALID_CLIENT_DOMAIN_NAMES:
        if domain in value:
            break
    else:
        if value in settings.TEST_EMAILS:
            return
        ','.join(settings.VALID_CLIENT_DOMAIN_NAMES)
        raise ValidationError(
            'A valid email should be from following domain names {0}.'.format(
                settings.VALID_CLIENT_DOMAIN_NAMES
            )
        )


class User(AbstractBaseUser):
    '''A User'''

    USER_TYPE_CHOICES = (
        (1, SUPER_USER),
        (2, OPERATOR),
        (3, TOKEN_USER),
        (4, AUDITOR),
    )
    email = models.EmailField(
        max_length=100, unique=True, validators=[validate_user_email_domain]
    )
    user_type = models.PositiveSmallIntegerField(
        default=2, choices=USER_TYPE_CHOICES
    )
    first_name = models.CharField(blank=False, max_length=20)
    last_name = models.CharField(blank=False, max_length=20)
    username = models.CharField(blank=False, max_length=200, unique=True)
    contact_number = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=200)
    pin_code = models.CharField(max_length=8)
    city = models.CharField(max_length=16)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    is_email_verified_by_user = models.BooleanField(default=False)
    email_confirmation_mail_sent_on = models.DateTimeField(null=True)
    account_activation_mail_sent_to_admin = models.DateTimeField(null=True)
    account_activation_replied_by_admin = models.DateTimeField(null=True)
    deactivated_on = models.DateTimeField(null=True)
    next_password_change_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    gsx_technician_id = models.CharField(max_length=100)
    gsx_user_name = models.CharField(max_length=100)
    gsx_auth_token = models.CharField(max_length=100)
    gsx_ship_to = models.CharField(max_length=100, default='0001026647')
    gsx_token_last_refreshed_on = models.DateTimeField(null=True)
    is_admin = models.BooleanField(default=False)  # a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'contact_number',
        'address',
        'pin_code',
        'city',
        'gsx_technician_id',
        'gsx_user_name',
        'gsx_ship_to',
        'gsx_auth_token',
    ]
    objects = UserManager()

    @property
    def full_name(self):
        'Get Full name of the user.'
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def need_to_change_password(self):
        'Check if user need to change his password.'
        return self.next_password_change_at < timezone.now()

    @property
    def is_staff(self):
        'Is the user a member of staff?'
        return self.is_admin

    @property
    def is_superuser(self):
        'is a superuser'
        return self.is_admin

    @property
    def role(self):
        for x, y in self.USER_TYPE_CHOICES:
            if x == self.user_type:
                return y

    def has_perm(self, perm, obj=None):
        'Yet To Be thought of'
        # Simplest possible answer: Yes, always
        return True

    def send_email_verification_mail_to_admin(self, value, send_email=True):
        self.is_email_verified_by_user = value
        if value:
            self.account_activation_mail_sent_to_admin = timezone.now()
            self.save()
        if send_email and value:
            return self.send_account_approval_request_to_authorities()

    def send_account_approval_request_to_authorities(self):
        template = settings.EMAIL_TEMPLATES.get('action')
        uid = http.urlsafe_base64_encode(encoding.force_bytes(self.pk))
        token = account_activation_token.make_token(self)
        account_approval_url = utils.get_url_for_account_approval_from_admin(
            uid, token
        )
        subject = 'Approve Account for user {0}'.format(self.full_name)
        message = """If you wish to allow this user to perform day to day
        usage of {0} portal then please click on the link bellow.""".format(
            settings.SITE_HEADER
        )
        user_action = 'Approve Account For {0} '.format(self.full_name)
        context = {
            'receiver_short_name': 'All',
            'summary': message,
            'detail': '',
            'action_name': user_action,
            'action_link': account_approval_url,
        }

        receivers = User.objects.all_superusers().values_list(
            'email', flat=True
        )
        if not receivers:
            receivers = [email for name, email in settings.ADMINS]
            logging.warning(
                'No SuperUser is Registed to the {} approval mail will be sent on admin emails {}'.format(
                    self, ','.join(receivers)
                )
            )
        else:
            logging.info(
                'user {} approval mail will be sent on admin emails {}'.format(
                    self.email, ','.join(receivers)
                )
            )
            utils.send_mail(subject, template, *receivers, **context)
        return receivers

    def send_email_verification_mail(self):
        template = settings.EMAIL_TEMPLATES.get('action')
        uid = http.urlsafe_base64_encode(encoding.force_bytes(self.pk))
        token = account_activation_token.make_token(self)
        email_verification = utils.get_url_for_email_verification(uid, token)
        subject = 'Verify your {0} email'.format(settings.SITE_HEADER)
        summary = """Please confirm your email address by
        clicking the link below."""
        details = """We may need to send you critical
        information about our service and it is important
        that we have an accurate email address."""

        user_action = 'Confirm your Email'
        context = {
            'receiver_short_name': self.get_short_name(),
            'summary': summary,
            'detail': details,
            'uid': uid,
            'token': token,
            'action_name': user_action,
            'action_link': email_verification,
        }
        logging.info(
            'user email verification mail will be sent on email {}'.format(
                self.email
            )
        )
        utils.send_mail(subject, template, self.email, **context)
        self.email_confirmation_mail_sent_on = timezone.now()
        self.save()

    def send_reset_password_link(self):
        template = settings.EMAIL_TEMPLATES.get('action')
        uid = http.urlsafe_base64_encode(encoding.force_bytes(self.pk))
        token = default_token_generator.make_token(self)
        reset_password_link = utils.get_url_password_reset(uid, token)
        subject = 'Reset you password for {0} email'.format(
            settings.SITE_HEADER
        )
        summary = """Please click on the bellow link to genarate your login password
        clicking the link below."""
        details = ' '

        user_action = 'Reset Your Password'
        context = {
            'receiver_short_name': self.get_short_name(),
            'summary': summary,
            'detail': details,
            'uid': uid,
            'token': token,
            'action_name': user_action,
            'action_link': reset_password_link,
        }
        logging.info(
            'user password reset mail will be sent on email {}'.format(
                self.email
            )
        )
        utils.send_mail(subject, template, self.email, **context)

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app app_label?'
        return True

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.full_name

    def increment_password_change_time(self, offset=settings.PASSWORD_AGE):
        '''
        Change Current User Password
        '''
        n_time = utils.time_by_adding_business_days(offset)
        self.next_password_change_at = n_time
        logging.info(
            'user {} next password change time set to {}'.format(
                self.email, self.next_password_change_at
            )
        )

    def toggle_activation(self, is_active):
        self.is_active = is_active
        self.save()
        logging.info(
            'user {} activation status changed to {}'.format(
                self.email, self.is_active
            )
        )
        attributes_changed.send(
            sender=self.__class__, user=self, attributes=['is_active']
        )

    def toggle_admin_status(self, is_admin):
        self.is_admin = is_admin
        self.save()
        logging.info(
            'user {} admin status changed to {}'.format(
                self.email, self.is_admin
            )
        )

    def refresh_gsx_token(self, gsx_token=None, gsx_ship_to=None):
        req = None
        result = None
        if gsx_token:
            req = GSXRequest(
                'authenticate',
                'token',
                self.gsx_user_name,
                gsx_token,
                self.gsx_ship_to
            )
        else:
            req = GSXRequest(
                'authenticate',
                'token',
                self.gsx_user_name,
                self.gsx_auth_token,
                self.gsx_ship_to
            )

        if req:
            result = req.handle_token_timeout(self)
        return result

    def __str__(self):
        return self.email


@receiver(attributes_changed)
def send_activation_mail_to_user(sender, user, attributes, **kwargs):
    if 'is_active' in attributes and getattr(user, 'is_active'):
        if not user.is_superuser:
            user.send_reset_password_link()

    if 'is_active' in attributes and not getattr(user, 'is_active'):
        template = settings.EMAIL_TEMPLATES.get('alert', None)
        subject = 'Your {0} account has been deactivate'.format(
            settings.SITE_HEADER
        )
        summary = """Your Account has been deactivate by the admin."""
        context = {
            'receiver_short_name': user.get_short_name(),
            'summary': summary,
        }
        utils.send_mail(subject, template, user.email, **context)
