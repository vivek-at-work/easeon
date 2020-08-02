# -*- coding: utf-8 -*-
import re
from core import utils
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.apps import apps


def validate_open_tickets(payload):
    email = payload.get('email')
    contact_number = payload.get('contact_number')
    Ticket = apps.get_model(utils.get_ticket_model())
    open_tickets = (
        Ticket.objects.filter(
            Q(customer__email=email)
            | Q(customer__contact_number=contact_number)
        )
        .open()
        .values_list('reference_number', flat=True)
    )
    if open_tickets:

        raise ValidationError(
            """This Customer has pending open tickets.Close them before proceeding for a new one {0}""".format(
                ','.join(open_tickets)
            )
        )
