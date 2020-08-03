# -*- coding: utf-8 -*-
import pyotp
from core import utils
from django.conf import settings
from django.core.validators import validate_email
from rest_framework.reverse import reverse

from .models import PyOTP


class OTPMixin(object):
    """
    Apply this mixin to Perform Various operations of PyOTP.
    """

    provision_uri = False

    def _get_random_base32_string(self):
        """Generate Random Base32 string

        """
        return pyotp.random_base32()

    def _insert_into_db(
        self, otp, secret=None, count=None, interval=None, data={}
    ):
        """

        :param secret: otp secret.
        :param count: hotp count.
        :param interval: totp interval
        :param data: other data (related to provisioning uri)
        :return: otp object
        """
        fields = {
            'otp': otp,
            'secret': secret,
            'count': count,
            'interval': interval,
        }

        # is provision settings is True only then save data into db
        if self.provision_uri is True:
            fields.update(**data)

        return PyOTP.objects.create(**fields)

    def _generate_hotp(self, count, provision_uri=False, data={}):
        """Generates counter-based OTPs

        """
        self.provision_uri = provision_uri
        base32string = self._get_random_base32_string()
        hotp = pyotp.HOTP(base32string)
        otp = hotp.at(count)

        # save data into db
        obj = self._insert_into_db(
            otp, secret=base32string, count=count, data=data
        )
        response = self._create_response(otp, obj, hotp, data)
        otp = response.get('otp')
        uid = response.get('otp_uuid')
        response['verify_url'] = 'core/verify-otp/hotp/{}'.format(uid)
        receiving_address = data.get('contact_number', None)
        is_valid_email = False
        # TODO: Handle Email Check More Gracefully.
        try:
            validate_email(receiving_address)
            is_valid_email = True
        except Exception:
            is_valid_email = False

        if not is_valid_email:
            utils.send_otp(receiving_address, otp)
        else:
            template = settings.EMAIL_TEMPLATES.get('alert')
            context = {
                'receiver_short_name': '',
                'summary': 'OTP for your login is {0}'.format(otp),
                'detail': """Please use given login otp
                            to login to {0}""".format(
                    settings.SITE_HEADER
                ),
                'action_name': otp,
            }
            subject = 'Login OTP for your {0} account'.format(
                settings.SITE_HEADER
            )
            utils.send_mail(subject, template, receiving_address, **context)
        del response['otp']
        return response

    def _generate_totp(self, interval, provision_uri=False, data={}):
        """Generates time-based OTPs

        """
        self.provision_uri = provision_uri
        base32string = self._get_random_base32_string()
        totp = pyotp.TOTP(base32string, interval=interval)
        otp = totp.now()

        # save data into db
        obj = self._insert_into_db(
            otp, secret=base32string, interval=interval, data=data
        )
        return self._create_response(otp, obj, totp, data)

    def _create_response(self, otp, instance, otp_type_obj, data):
        """Create Response

        :param instance: pytop model instance
        :param otp_type_obj: hotp/totp object
        :param data: other data (related to provisioning uri)
        :return: response dict
        """
        response = {'otp_uuid': str(instance.uuid), 'otp': otp}

        # Generate provision uri if settings is True
        if self.provision_uri is True:
            provisioning_uri = otp_type_obj.provisioning_uri(**data)
            response = {'provisioning_uri': provisioning_uri}

        return response
