# -*- coding: utf-8 -*-
import http
import json
import logging
import time
import urllib
from os import path

from core.utils import get_uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import encoding, timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from .error_code import UNAUTHORIZED,SESSION_IDLE_TIMEOUT
from .gsx_exceptions import GSXResourceNotAvailableError

logger = logging.getLogger()

class GSXRequestUAT:
    def __init__(self,
        service,
        method,
        gsx_user_name,
        auth_token, ship_to):
        self.service = service
        self.method = method
        self.gsx_user_name = gsx_user_name.lower()
        self.auth_token = auth_token
        self.ship_to = ship_to
        self.url = self.get_resource_url(self.service, self.method)
        self.can_handle_token_timout = True
        self.is_connectivity_request = False
        if method == "check":
            self.is_connectivity_request = True

    def _process_errors(self, message):
        error_codes = []
        if message and self.is_json(message):
            message = json.loads(message)
            try:
                if "errors" in message:
                    for error in message["errors"]:
                        error_codes.append(error.get("code"))
                if "errorId" in message and "errors" in message:
                    logging.error(
                        "UAT ** Error Response %s received from GSX for url %s", message, self.url
                    )
                is_unauthorized = (UNAUTHORIZED in error_codes) or (SESSION_IDLE_TIMEOUT in error_codes)
                return message, error_codes, is_unauthorized
            except Exception as e:
                logging.error(
                    "UAT **  Could not process %s received from GSX for url %s and %s",
                    message,
                    self.url,
                    e,
                )
        return message, [], True

    def get_connection(self):
        cert , key , url, sold_to, ship_to = settings.GSX_SETTINGS_UAT
        if path.exists(cert) and path.exists(key):
            return http.client.HTTPSConnection(
                url, cert_file=cert, key_file=key
            )
        else:
            raise GSXResourceNotAvailableError()

    def get_resource_url(self, service, method):
        prefix = "/gsx/api/"
        if service == "authenticate":
            prefix = "/api/"

        resource = "{}{}".format(prefix,service)
        if method:
            resource = "{}{}/{}".format(prefix,service, method)
        return resource

    def get_headers(self,auth_token, ship_to):
        cert , key , url, sold_to, _ = settings.GSX_SETTINGS_UAT
        head = {
            "X-Apple-SoldTo": sold_to,
            "X-Apple-ShipTo": ship_to,
            "X-Apple-Trace-ID": str(get_uuid()),
            "X-Apple-Service-Version": "v2",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Apple-Client-Locale": "en-US",
        }
        if ship_to:
            head["X-Apple-ShipTo"] = ship_to
        if auth_token:
            head["X-Apple-Auth-Token"] = auth_token
        return head

    def is_json(self,data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    def handle_token_timeout(self, user=None):
        logging.info(
            "******************REFRESH GSX TOKEN REQUEST*****************************"
        )
        self.can_handle_token_timout = False
        connection = self.get_connection()
        logging.info(
            "UAT **   GSX token refresh request received for username %s and token %s",
            self.gsx_user_name,
            self.auth_token,
        )
        payload_string = json.dumps(
            {"userAppleId": self.gsx_user_name, "authToken": self.auth_token}
        )
        headers_dict = self.get_headers(self.auth_token, self.ship_to)
        url = self.get_resource_url("authenticate", "token")
        connection.request("POST", url, body=payload_string, headers=headers_dict)
        logging.info(
            "UAT **  GSX Refresh Token Request %s for endpoint %s with headers %s and data %s",
            "POST",
            url,
            headers_dict,
            payload_string,
        )
        response = connection.getresponse()
        output = response.read()
        result = json.loads(output) if self.is_json(output) else output
        logging.info(
            "UAT ** GSX Refresh Token Response %s for endpoint %s with headers %s and data %s",
            result,
            url,
            headers_dict,
            payload_string,
        )
        if "authToken" in result:
            r1 = get_user_model().objects.filter(gsx_user_name=self.gsx_user_name)
            r1.update(
                gsx_auth_token=result["authToken"],
                gsx_token_last_refreshed_on=timezone.now(),
            )
            self.auth_token = result["authToken"]
            return True
        return False

    def _send_request(self, method, url, payload_string=None):
        connection = self.get_connection()
        if method == "GET":
            connection.request(
                method, url,
                headers=self.get_headers(self.auth_token, self.ship_to)
            )
            logging.info(
                " UAT ** GSX Request Method  %s for endpoint %s with headers %s",
                method,
                url,
                self.get_headers(self.auth_token, self.ship_to),
            )
        if method == "POST":
            connection.request(
                method,
                url,
                body=payload_string,
                headers=self.get_headers(self.auth_token, self.ship_to),
            )
            logging.info(
                "UAT **  GSX Request Method  %s for endpoint %s with headers %s and data %s",
                method,
                url,
                self.get_headers(self.auth_token, self.ship_to),
                payload_string,
            )
        response = connection.getresponse()
        response_headers = response.headers
        output = response.read()
        if self.is_connectivity_request:
            message = json.loads(output) if self.is_json(output) else output
            return message, None, None
        else:
            message, error_codes, is_unauthorized = self._process_errors(output)
        if (
            is_unauthorized
            and self.can_handle_token_timout
            and not self.is_connectivity_request
        ):
            if self.handle_token_timeout():
                return self._send_request(method, url, payload_string)
        return message, error_codes, is_unauthorized, response_headers

    def get(self, **data):
        if data:
            query_string = urllib.parse.urlencode(data)
            url = self.url + "?" + query_string
        else:
            url = self.url
        (message, error_codes, is_unauthorized, response_headers) = self._send_request(
            "GET", url
        )
        if is_unauthorized:
            raise ValidationError("You are not authrized.")
        if error_codes:
            raise ValidationError(message)

        return message

    def post(self, **kwargs):
        data = kwargs
        if "payload" in kwargs.keys():
            data = kwargs["payload"]
        return_headers = "return_headers" in kwargs.keys()
        if return_headers:
            del kwargs["return_headers"]
        (message, error_codes, is_unauthorized, response_headers) = self._send_request(
            "POST", self.url, json.dumps(data)
        )
        if is_unauthorized:
            raise ValidationError("You are not authrized.")
        if error_codes:
            raise ValidationError(message)
        if return_headers:
            return response_headers, message
        return message
