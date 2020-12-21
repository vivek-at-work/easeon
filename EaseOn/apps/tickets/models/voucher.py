# -*- coding: utf-8 -*-
"""voucher models"""
from core import utils
from core.models import BaseModel
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .ticket import Ticket


class Voucher(BaseModel):
    """A voucher"""

    cash = models.FloatField(null=True, blank=True, default=0.0)
    cheque = models.FloatField(null=True, blank=True, default=0.0)
    online_payment = models.FloatField(null=True, blank=True, default=0.0)
    cc = models.FloatField(null=True, blank=True, default=0.0)
    online_payment_reference_number = models.CharField(
        blank=True, null=True, max_length=50
    )
    reference_number = models.CharField(
        unique=True, blank=False, null=False, max_length=50
    )
    towards = models.CharField(blank=True, max_length=100)
    online_payment_date_time = models.DateTimeField(null=True)
    note = models.CharField(blank=True, max_length=2400)
    is_cancelled = models.BooleanField(default=False)
    ticket = models.ForeignKey(
        Ticket, related_name="vouchers", on_delete=models.CASCADE
    )
    customer_signature = models.ImageField(
        upload_to="customer_signatures/vouchers", null=True, blank=True
    )

    @property
    def total_amount(self):
        return self.cash + self.cheque + self.online_payment + self.cc

    @property
    def actual_payment_modes(self):
        mode = []
        if self.cash:
            mode.append("Cash")
        if self.cheque:
            mode.append("Cheque")
        if self.online_payment:
            mode.append("Online Payment")
        if self.cc:
            mode.append("Credit Card")
        return mode

    class Meta:
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"
        ordering = ["-id"]

    def __str__(self):
        return self.reference_number


@receiver(pre_save, sender=Voucher)
def set_reference_number_for_voucher(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        suffix = instance.ticket.vouchers.count() + 1
        reference_number = "{0}-{1}-{2}".format(
            instance.ticket.organization.code, instance.ticket.id, suffix
        )
        instance.reference_number = reference_number


@receiver(post_save, sender=Voucher)
def send_mail_to_subscribers(sender, instance, created, **kwargs):
    template = settings.EMAIL_TEMPLATES.get("alert")
    summary = "Please find the voucher details on ticket {0} as bellow".format(
        instance.ticket
    )
    details = """Towards = {0}
                 Actual Payment Modes = {1}
                 Total Amount = {2}
                 Comment = {3}
                 Has Cancelled ={4}

    """.format(
        instance.towards,
        ",".join(instance.actual_payment_modes),
        instance.total_amount,
        instance.note,
        "Yes" if instance.is_cancelled else "NO",
    )
    if created:
        subject = "New Voucher on Ticket {} from {} ".format(
            instance.ticket, instance.created_by
        )
    else:
        subject = "Existing Voucher on Ticket {}  updated from {} ".format(
            instance.ticket, instance.last_modified_by
        )
    context = {"receiver_short_name": "All", "summary": summary, "detail": details}
    utils.send_mail(
        subject,
        template,
        list(instance.ticket.subscribers.values_list("email", flat=True)),
        **context
    )
