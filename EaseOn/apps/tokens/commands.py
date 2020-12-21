import requests
import json
from tokens import models, serializers
def send_token_display_refresh_command(token):
    url = "https://www.easeon.in:8000/api"
    payload={
            "organization": token.organization.token_machine_location_code,
            "command" : "reload"
    }
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload)

def send_token_display_call_command(**token):
    url = "https://www.easeon.in:8000/api"
    payload={
            "organization": token['location_code'],
            "command" : "call",
            "data":token
    }
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers,  json=payload)