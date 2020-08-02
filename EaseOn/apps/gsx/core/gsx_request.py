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

from .error_code import UNAUTHORIZED
from .gsx_exceptions import GSXResourceNotAvailableError

logger = logging.getLogger('easeOn')
GSX_CERT_FILE_PATH = settings.GSX_CERT_FILE_PATH
GSX_KEY_FILE_PATH = settings.GSX_KEY_FILE_PATH
GSX_URL = settings.GSX_URL
GSX_SOLD_TO = settings.GSX_SOLD_TO
GSX_SHIP_TO = settings.GSX_SHIP_TO
GSX_ENV = settings.GSX_ENV


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def get_resource_url(service, method):
    resource = '/gsx/api/{0}'.format(service)
    if method:
        resource = '/gsx/api/{0}/{1}'.format(service, method)
    return resource


def get_connection(gsx_user_name, auth_token):
    if path.exists(GSX_CERT_FILE_PATH) and path.exists(GSX_KEY_FILE_PATH):
        return http.client.HTTPSConnection(
            GSX_URL, cert_file=GSX_CERT_FILE_PATH, key_file=GSX_KEY_FILE_PATH,
        )
    else:
        raise GSXResourceNotAvailableError()


def get_headers(auth_token, ship_to):
    head = {
        'X-Apple-SoldTo': GSX_SOLD_TO,
        'X-Apple-ShipTo': ship_to,
        'X-Apple-Trace-ID': str(get_uuid()),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    if ship_to:
        head['X-Apple-ShipTo'] = ship_to
    if auth_token:
        head['X-Apple-Auth-Token'] = auth_token
    return head


def _prepare_response(gsx_user_name, **kwargs):
    raw_response = {
        'ENV_USED': GSX_ENV,
        'AppleID': gsx_user_name,
    }
    raw_response.update(kwargs)
    return raw_response


class GSXRequest:
    def __init__(self, service, method, gsx_user_name, auth_token, ship_to):
        self.service = service
        self.method = method
        self.gsx_user_name = gsx_user_name
        self.auth_token = auth_token
        self.ship_to = ship_to
        self.url = get_resource_url(self.service, self.method)
        self.can_handle_token_timout = True
        self.is_connectivity_request = False
        if method == 'check':
            self.is_connectivity_request = True

    def _process_errors(self, message):
        error_codes = []
        message = json.loads(message)
        try:
            if 'errors' in message:
                for error in message['errors']:
                    error_codes.append(error.get('code'))
            if 'errorId' in message and 'errors' in message:
                logging.error(
                    'Error Response %s received from GSX for url %s',
                    message,
                    self.url,
                )
            is_unauthorized = UNAUTHORIZED in error_codes
            return message, error_codes, is_unauthorized
        except Exception as e:
            logging.error(
                'Could not process %s received from GSX for url %s due to',
                message,
                self.url,
                e,
            )

    def handle_token_timeout(self, user=None):
        logging.info(
            '******************REFRESH GSX TOKEN REQUEST*****************************'
        )
        self.can_handle_token_timout = False
        connection = get_connection(self.gsx_user_name, self.auth_token)
        logging.info(
            'GSX token refresh request received for username %s and token %s',
            self.gsx_user_name,
            self.auth_token,
        )
        payload_string = json.dumps(
            {'userAppleId': self.gsx_user_name, 'authToken': self.auth_token}
        )
        headers_dict = get_headers(self.auth_token, self.ship_to)
        url = get_resource_url('authenticate', 'token')
        connection.request(
            'POST', url, body=payload_string, headers=headers_dict,
        )
        logging.info(
            'GSX Refresh Token Request %s for endpoint %s with headers %s and data %s',
            'POST',
            url,
            headers_dict,
            payload_string,
        )
        response = connection.getresponse()
        output = response.read()
        result = json.loads(output) if is_json(output) else output
        logging.info(
            'GSX Refresh Token Response %s for endpoint %s with headers %s and data %s',
            result,
            url,
            headers_dict,
            payload_string,
        )
        if 'authToken' in result:
            r1 = get_user_model().objects.filter(
                gsx_user_name=self.gsx_user_name
            )
            r1.update(
                gsx_auth_token=result['authToken'],
                gsx_token_last_refreshed_on=timezone.now(),
            )
            self.auth_token = result['authToken']
            return True
        return False

    def _send_request(self, method, url, payload_string=None):
        connection = get_connection(self.gsx_user_name, self.auth_token)
        if method == 'GET':
            connection.request(
                method, url, headers=get_headers(self.auth_token, self.ship_to)
            )
            logging.info(
                'GSX Request Method  %s for endpoint %s with headers %s',
                method,
                url,
                get_headers(self.auth_token, self.ship_to),
            )
        if method == 'POST':
            connection.request(
                method,
                url,
                body=payload_string,
                headers=get_headers(self.auth_token, self.ship_to),
            )
            logging.info(
                'GSX Request Method  %s for endpoint %s with headers %s and data %s',
                method,
                url,
                get_headers(self.auth_token, self.ship_to),
                payload_string,
            )
        response = connection.getresponse()
        output = response.read()
        if self.is_connectivity_request:
            message = json.loads(output) if is_json(output) else output
            return message, None, None
        else:
            message, error_codes, is_unauthorized = self._process_errors(
                output
            )
        if (
            is_unauthorized
            and self.can_handle_token_timout
            and not self.is_connectivity_request
        ):
            if self.handle_token_timeout():
                return self._send_request(method, url, payload_string)
        return message, error_codes, is_unauthorized

    def get(self, **data):
        if data:
            query_string = urllib.parse.urlencode(data)
            url = self.url + '?' + query_string
        else:
            url = self.url
        message, error_codes, is_unauthorized = self._send_request('GET', url)
        return message

    def post(self, **kwargs):
        data = kwargs
        if 'payload' in kwargs.keys():
            data = kwargs['payload']
        message, error_codes, is_unauthorized = self._send_request(
            'POST', self.url, json.dumps(data)
        )
        return message
