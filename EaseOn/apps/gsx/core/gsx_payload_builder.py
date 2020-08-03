# -*- coding: utf-8 -*-
from rest_framework import serializers


def get_device(ticket):
    return {'id': ticket.device.identifier}


def get_notes(ticket):
    return [
        {
            'type': 'CUSTOMER_INTAKE_NOTES',
            'content': ticket.issue_reported_by_customer,
        }
    ]


def get_repair_classification(ticket):
    return 'SINGLE'


def get_repair_type(ticket):
    return 'CRBR'


def get_service_non_repair_type(ticket):
    return 'NTF'


def get_unit_receive_date_time(ticket):
    return ticket.created_on


def get_repair_flags(ticket):
    return {'requestReviewByApple': True, 'markComplete': True}


def get_reference_number(ticket):
    return ticket.reference_number


def get_purchase_order_number(ticket):
    return ticket.reference_number


def get_component_issues(ticket):
    return [
        {
            'componentCode': '26099',
            'reproducibility': 'A',
            'priority': 1,
            'type': 'TECH',
            'issueCode': 'IP044',
            'order': 1,
        }
    ]


def get_technician_id(user):
    return user.gsx_technician_id


def get_customer_info(ticket):
    customer = ticket.customer
    return {
        'firstName': customer.first_name,
        'lastName': customer.last_name,
        'primaryPhone': customer.contact_number,
        'emailAddress': customer.email,
        'sendSMSOnPrimaryPhone': True,
        'address': [
            {
                'line4': 'string',
                'city': 'string',
                'countryCode': 'IND',
                'postalCode': '411007',
                'stateCode': 'UP',
                'line3': 'string',
                'line2': 'string',
                'line1': 'string',
            }
        ],
        'companyName': customer.company_name,
        'type': 'VAR',
    }
