# -*- coding: utf-8 -*-
import http.client

from django.conf import settings

APIKEY = settings.SMS_BACKEND_KEY


class TwoFactorIn(object):
    @staticmethod
    def get_balance():
        conn = http.client.HTTPConnection('2factor.in')
        payload = ''
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        conn.request(
            'GET', '/API/V1/{}/BAL/SMS'.format(APIKEY), payload, headers
        )
        res = conn.getresponse()
        data = res.read()
        return data.decode('utf-8')

    @staticmethod
    def send(number, otp, template_name='LOGIN_OTP'):
        conn = http.client.HTTPConnection('2factor.in')
        payload = ''
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        conn.request(
            'GET',
            '/API/V1/{}/SMS/{}/{}/{}'.format(
                APIKEY, number, otp, template_name
            ),
            payload,
            headers,
        )

        res = conn.getresponse()
        data = res.read()
        return data.decode('utf-8')

    @staticmethod
    def check_balance():
        conn = http.client.HTTPConnection('2factor.in')
        payload = ''
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        conn.request(
            'GET',
            '/API/V1/{}/BAL/SMS'.format(APIKEY),
            payload,
            headers,
        )

        res = conn.getresponse()
        data = res.read()
        return data.decode('utf-8')
