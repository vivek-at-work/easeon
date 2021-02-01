# -*- coding: utf-8 -*-
import json

import requests
from tokens import models, serializers
from django.conf import settings

REAL_TIME_API_URL = settings.REAL_TIME_API_URL

def send_token_display_refresh_command(token):
    
    url =REAL_TIME_API_URL
    payload = {
        "organization": token.organization.token_machine_location_code,
        "command": "reload",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, json=payload)
    return response


def send_token_display_call_command(**token):
    url = REAL_TIME_API_URL
    payload = {"organization": token["location_code"], "command": "call", "data": token}
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, json=payload)
    return response
