# -*- coding: utf-8 -*-
from core.models import BaseManager, BaseModel
from django.db import models

SLA_TYPE_CHOICES = (
    ('TICKET_SLA', 'Ticket SLA'),
    ('DELIVERY_SLA', 'Delivery SLA'),
    ('PHONE_LOAN_AGREEMENT', 'Phone Loan Agreement'),
)


class SLAManager(BaseManager):
    def get_default_ticket_sla(self):
        return self.get_queryset().filter(
            sla_type='TICKET_SLA', is_default=True
        )

    def get_default_delivery_sla(self):
        return self.get_queryset().filter(
            sla_type='DELIVERY_SLA', is_default=True
        )

    def get_queryset(self):
        return super(SLAManager, self).get_queryset()


class SLA(BaseModel):
    """A SLA"""

    sla_type = models.CharField(
        max_length=100, choices=SLA_TYPE_CHOICES, default='TICKET_SLA'
    )
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    objects = SLAManager()

    def save(self, *args, **kwargs):
        if self.is_default:
            SLA.objects.filter(sla_type=self.sla_type).update(is_default=False)
        return super(SLA, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'SLA'
        verbose_name_plural = 'SLAs'

    def __str__(self):
        return str(self.name)


class Term(BaseModel):
    """A SLA Term"""

    sla = models.ManyToManyField(SLA, related_name='terms')
    statement = models.TextField()
    heading = models.TextField(null=True, max_length=2048)

    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return self.statement
