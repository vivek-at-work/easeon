# -*- coding: utf-8 -*-
from core import utils
from core.models import BaseModel, User
from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .signals import membership_attributes_changed


class Holiday(BaseModel):
    organization = models.ForeignKey(
        'Organization', on_delete=models.DO_NOTHING, related_name='holidays'
    )
    date = models.DateField()
    description = models.CharField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['organization', 'date'],
                condition=Q(is_deleted=False),
                name='organization_holiday_unique_is_deleted',
            )
        ]


@receiver(post_save, sender=Holiday)
def send_holiday_notifications(sender, instance, *args, **kwargs):
    template = settings.EMAIL_TEMPLATES.get('alert', None)
    subject = 'New Holiday Details Updated on {} '.format(settings.SITE_HEADER)
    summary = """A Non working day {0} have been mentioned for {1} """.format(
        instance.date, instance.organization
    )
    details = (
        'This Date will not be allowed as expected delivery date here after'
    )
    action_name = instance.date

    context = {
        'receiver_short_name': instance.organization.manager.get_short_name(),
        'summary': summary,
        'detail': details.format(),
        'action_name': action_name,
    }
    utils.send_mail(
        subject, template, instance.organization.manager.email, **context
    )
