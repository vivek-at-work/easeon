# -*- coding: utf-8 -*-
def format_customer(customer):
    return {
        'firstName': customer.first_name,
        'lastName': customer.last_name,
        'primaryPhone': customer.contact_number,
        'emailAddress': customer.email,
        'sendSMSOnPrimaryPhone': True,
        'address': [
            {
                'city': customer.city,
                'countryCode': customer.country,
                'postalCode': customer.pin_code,
                'stateCode': customer.state,
                'line3': customer.street,
                'line2': customer.address_line_2,
                'line1': customer.address_line_1,
            }
        ],
    }


def format_device(device, add_configuration=False):
    return {
        'configuration': {
            'hardDiskSize': '32GB',
            'osVersion': 'someOs',
            'ramSize': '4GB',
        },
        'id': device.identifier,
    }
