# -*- coding: utf-8 -*-
import http.client
import ssl

from django.conf import settings

APIKEY = settings.SMS_BACKEND_KEY


class TwoFactorIn(object):
    @staticmethod
    def send(number, otp, template_name="LOGIN_OTP"):
        conn = http.client.HTTPConnection("2factor.in")
        payload = ""
        headers = {"content-type": "application/x-www-form-urlencoded"}

        conn.request(
            "GET",
            "/API/V1/{}/SMS/{}/{}/{}".format(APIKEY, number, otp, template_name),
            payload,
            headers,
        )

        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    @staticmethod
    def check_balance():
        conn = http.client.HTTPConnection("2factor.in")
        payload = ""
        headers = {"content-type": "application/x-www-form-urlencoded"}
        conn.request("GET", "/API/V1/{}/BAL/SMS".format(APIKEY), payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")


class APPIndia(object):
    @staticmethod
    def send(number, message, template_name="LOGIN_OTP"):
        import urllib

        conn = http.client.HTTPSConnection("app.indiasms.com")
        payload = ""
        headers = {}
        conn.request(
            "GET",
            "/sendsms/sendsms.php?username={}&password={}&type=TEXT&sender={}&mobile={}&message={}".format(
                settings.APP_INDIA_USERNAME,
                settings.APP_INDIA_PASSWORD,
                settings.APP_INDIA_SENDER,
                number,
                urllib.parse.quote(message),
            ),
            payload,
            headers,
        )
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    @staticmethod
    def check_balance():
        conn = http.client.HTTPConnection("2factor.in")
        payload = ""
        headers = {"content-type": "application/x-www-form-urlencoded"}
        conn.request("GET", "/API/V1/{}/BAL/SMS".format(APIKEY), payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
