# -*- coding: utf-8 -*-
from core import utils
from core.models import BaseModel
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .ticket import Ticket


class Comment(BaseModel):
    value = models.CharField(max_length=2000)
    ticket = models.ForeignKey(
        Ticket, related_name="comments", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-id']

    def __str__(self):
        return self.value


@receiver(post_save, sender=Comment)
def send_mail_to_subscribers(sender, instance, created, **kwargs):
    template = settings.EMAIL_TEMPLATES.get("alert")
    details = instance.value
    summary = """'Please find the comment on ticket as bellow."""
    if created:
        subject = "New Comment on Ticket {} from {} ".format(
            instance.ticket, instance.created_by
        )
    else:
        subject = "Existing Comment on Ticket {}  updated from {} ".format(
            instance.ticket, instance.last_modified_by
        )
    context = {"receiver_short_name": "All", "summary": summary, "detail": details}
    utils.send_mail(
        subject,
        template,
        list(instance.ticket.subscribers.values_list("email", flat=True)),
        **context
    )
