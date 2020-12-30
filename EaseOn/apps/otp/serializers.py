# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pyotp
from otp import mixins
from rest_framework import serializers


class NoneSerializer(serializers.Serializer):
    pass


class TotpSerializer(mixins.OTPMixin, serializers.Serializer):
    """TOTP serializer"""

    time = serializers.IntegerField(
        required=True, help_text="OTP Validity-Time (in seconds)."
    )

    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        interval = validated_data.pop("time")
        return self._generate_totp(interval, data=validated_data)


class HotpSerializer(mixins.OTPMixin, serializers.Serializer):
    """HOTP serializer"""

    count = serializers.IntegerField(default=1, help_text="OTP Counter.")
    # email = serializers.EmailField(
    #     required=True, help_text='Email to Send OTP TO.'
    # )
    contact_number = serializers.CharField(
        required=False, allow_blank=True, help_text="Contact Number to Send OTP TO."
    )
    otp_for = serializers.CharField(
        required=False, allow_blank=True, help_text="Name of the OTP Owner/Generator."
    )

    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        count = validated_data.pop("count")
        response = self._generate_hotp(count, data=validated_data)
        return response


class ProvisionUriSerializer(serializers.Serializer):
    """Serializer for provisioning serializer."""

    name = serializers.CharField(required=True, help_text="name of the account")
    issuer_name = serializers.CharField(help_text="name of the OTP issuer")


class TOTPProvisionUriSerializer(TotpSerializer, ProvisionUriSerializer):
    """Serializer for provisioning serializer + TOTP."""

    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        interval = validated_data.pop("time")
        return self._generate_totp(interval, provision_uri=True, data=validated_data)


class HOTPProvisionUriSerializer(HotpSerializer, ProvisionUriSerializer):
    """Serializer for provisioning serializer + HOTP."""

    initial_count = serializers.CharField(
        default=0, help_text="starting counter value, defaults to 0"
    )

    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        count = validated_data.pop("count")
        return self._generate_hotp(count, provision_uri=True, data=validated_data)


class VerifyOtpSerializer(serializers.Serializer):
    """Serializer used to verify OTP"""

    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField()
    contact_number = serializers.CharField(required=True)

    def verify_otp(self, otp, obj, otp_type):
        """

        :param otp_type:
        :return:
        """
        if otp_type == "hotp" and obj.count:
            hotp = pyotp.HOTP(obj.secret)
            if hotp.verify(otp, obj.count):
                return True
        elif otp_type == "totp" and obj.interval:
            totp = pyotp.TOTP(obj.secret, interval=obj.interval)
            return totp.verify(otp)
        return False


class VerifyCustomerOtpSerializer(serializers.Serializer):
    """Serializer used to verify OTP"""

    otp = serializers.CharField(required=True)
    contact_number = serializers.CharField(required=True)

    def verify_otp(self, otp, obj, otp_type):
        """

        :param otp_type:
        :return:
        """
        if otp_type == "hotp" and obj.count:
            hotp = pyotp.HOTP(obj.secret)
            if hotp.verify(otp, obj.count):
                return True
        elif otp_type == "totp" and obj.interval:
            totp = pyotp.TOTP(obj.secret, interval=obj.interval)
            return totp.verify(otp)
        return False
