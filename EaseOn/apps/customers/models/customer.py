# -*- coding: utf-8 -*-
from core import utils
from core.models import BaseModel
from django.apps import apps
from django.db import models
from django.utils import timezone


class Customer(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(blank=True, null=True, max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=60)
    address_line_2 = models.CharField(blank=True, null=True, max_length=40)
    street = models.CharField(max_length=60)
    email = models.EmailField()
    contact_number = models.CharField(max_length=50)
    alternate_contact_number = models.CharField(max_length=50, blank=True, null=True)
    last_visit_on = models.DateTimeField(null=True)
    customer_type = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    token_number = models.CharField(max_length=100)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def communication_address(self):
        return "{0} {1} {2} {3} {4} {5} {6}".format(
            self.address_line_1,
            self.address_line_2,
            self.street,
            self.city,
            self.state,
            self.country,
            self.pin_code,
        )

    @property
    def open_tickets(self):
        Ticket = apps.get_model(utils.get_ticket_model())
        return Ticket.objects.filter(
            customer__email=self.email, customer__contact_number=self.contact_number
        ).open()

    @property
    def user_messages(self):
        open_tickets = self.open_tickets.values_list("reference_number", flat=True)
        if open_tickets:
            return """This Customer has pending open tickets.Close them beforeproceeding for a new one {0}""".format(
                ",".join(open_tickets)
            )

    @property
    def time_since_last_visit(self):
        return timezone.localtime() - self.last_visit_on

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
