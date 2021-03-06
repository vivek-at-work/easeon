# -*- coding: utf-8 -*-
import datetime

import pytz
from core.models import BaseManager, BaseModel, BaseQuerySet
from core.utils import send_mail, workday
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone as dtz
from reporting import (
    LoanerRecordReport,
    OrderLineReport,
    SMTPReportTarget,
    StatusReport,
)

from .rights import OrganizationRights


class Organization(BaseModel):
    """An Organization """

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200, default="India")
    token_machine_location_code = models.CharField(max_length=200)
    email = models.EmailField()
    contact_number = models.CharField(max_length=200)
    timings = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    timezone = models.CharField(default="IST", max_length=128)
    manager = models.ForeignKey(
        get_user_model(), related_name="managed_locations", on_delete=models.DO_NOTHING
    )
    users = models.ManyToManyField(
        get_user_model(),
        through="OrganizationRights",
        through_fields=("organization", "user"),
    )
    gsx_ship_to = models.CharField(max_length=20)
    latitude = models.CharField(max_length=100,null=True)
    longitude = models.CharField(max_length=100,null=True)


    class Meta:
        verbose_name = "Service Centre"
        verbose_name_plural = "Service Centres"
        swappable = "ORGANIZATIONS_ORGANIZATION_MODEL"

        constraints = [
            UniqueConstraint(
                fields=["email"],
                condition=Q(is_deleted=False),
                name="email_unique_is_deleted",
            ),
            UniqueConstraint(
                fields=["contact_number"],
                condition=Q(is_deleted=False),
                name="contact_number_unique_is_deleted",
            ),
            UniqueConstraint(
                fields=["code"], condition=Q(is_deleted=False), name="code_is_deleted"
            ),
            UniqueConstraint(
                fields=["token_machine_location_code"],
                condition=Q(is_deleted=False),
                name="token_machine_location_code_unique_is_deleted",
            ),
        ]

    @property
    def communication_address(self):
        return "{0} {1} {2} {3} {4}".format(
            self.address,
            self.city,
            self.state,
            self.country,
            self.pin_code,
        )
    
    def get_available_loaner_devices(self):
        return self.loaner_inventory_items.all().available()

    def get_available_repair_items(self):
        return self.repair_inventory_items.all().available()

    def get_expected_delivery_date(self, add_days, from_date=dtz.now()):
        start_date = from_date.date()
        start_time = from_date.time()
        end_date = workday(
            start_date, add_days, self.holidays.all().values_list("date", flat=True)
        )
        return datetime.datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            start_time.hour,
            start_time.minute,
            start_time.second,
            tzinfo=pytz.UTC,
        )

    def __str__(self):
        return self.code

    @property
    def dashboard(self):
        dashboard_data = {}
        count = [
            {
                "order": 1,
                "heading": "Tickets Created Today",
                "value": self.tickets.all().created_between().count(),
            },
            {
                "order": 2,
                "heading": "Tickets Closed Today",
                "value": self.tickets.all().closed_between().count(),
            },
            {
                "order": 3,
                "heading": "Vouchers Created Today",
                "value": self.vouchers.all().created_between().count(),
            },
            {
                "order": 4,
                "heading": "Due Ticket For Today",
                "value": self.tickets.all().due_between().count(),
            },
        ]
        dashboard_data["counts"] = count
        return dashboard_data


@receiver(post_save, sender=Organization)
def onOrganizationSave(sender, instance, *args, **kwargs):
    template = settings.EMAIL_TEMPLATES.get("alert")
    details = """We are glad to have the chance to host a
        new service provider {0}-({1}).
        With easeOn, you can always expect to
        be welcomed with great services every time.""".format(
        instance.name, instance.code
    )

    summary = """A New Service Provider has been added to {0}.""".format(
        settings.SITE_HEADER
    )
    if not kwargs.get("created", False):
        details = """We are glad to inform you that organization details
        have been updated for {0}-({1}).
        With easeOn, you can always expect to
        be welcomed with great services every time.""".format(
            instance.name, instance.code
        )

        summary = """A Organization Details have been updated to {0}.""".format(
            settings.SITE_HEADER
        )

    context = {
        "receiver_short_name": "All",
        "summary": summary,
        "detail": details,
        "action_name": "View",
    }
    subject = summary
    # send_mail(
    #     subject, template, *get_user_model().objects.all_superusers_email(), **context
    # )


@receiver(post_save, sender=Organization)
def delete_if_managers_have_rights(sender, instance, *args, **kwargs):
    instance.memberships.all().filter(user=instance.manager).delete()
