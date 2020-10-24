# -*- coding: utf-8 -*-
from core.models import BaseModel
from core.utils import send_token_to_customer
from django.db import models, connection
from organizations.models import Organization
from django.contrib.auth import get_user_model
from websocket import create_connection


class Token(BaseModel):
    """A Service Token"""

    organization = models.ForeignKey(
        Organization,
        related_name='tokens',
        editable=False,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    location_code = models.CharField(max_length=100)
    token_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    invited_by = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name='received_tokens',
        on_delete=models.DO_NOTHING,
    )
    counter_number = models.IntegerField(null=True)
    contact_number = models.CharField(blank=True, null=True, max_length=50)
    invite_sent_on = models.DateTimeField(null=True)
    is_present = models.BooleanField(default=False)

    def send_token_number_by_sms(self):
        send_token_to_customer(
            self.contact_number, str(self.token_number).rjust(4, "0")
        )

    def can_invite(self, user):
        return (self.invited_by is None) or (self.invited_by == user)

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                'TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table)
            )
