# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models

from .ticket import Ticket


class Feedback(BaseModel):
    """
    Represents a Customer Feedback received on their
    experience with  the service provided to them.
    """

    parameter = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    ticket = models.ForeignKey(
        Ticket, related_name='feedbacks', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Customer Feedback'
        verbose_name_plural = 'Customer Feedbacks'

    def __unicode__(self):
        return self.value
