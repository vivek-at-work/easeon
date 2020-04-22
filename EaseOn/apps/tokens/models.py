# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from organizations.models import Organization


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
    city = models.CharField(max_length=50, blank=True, null=True,)
    country = models.CharField(max_length=50, blank=True, null=True,)
    state = models.CharField(max_length=50, blank=True, null=True,)
    address_line_1 = models.CharField(max_length=60)
    address_line_2 = models.CharField(blank=True, null=True, max_length=40)
    street = models.CharField(blank=True, null=True, max_length=60)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(blank=True, null=True, max_length=50)
    pin_code = models.CharField(max_length=50, blank=True, null=True,)
