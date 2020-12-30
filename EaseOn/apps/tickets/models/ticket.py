# -*- coding: utf-8 -*-
import random
from datetime import date, datetime, time

from core import utils
from core.models import BaseManager, BaseModel, BaseQuerySet, User
from core.utils import (
    account_activation_token,
    get_random_string,
    send_sms,
    time_by_adding_business_days,
)
from customers.models import Customer
from devices.models import Device
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import encoding, http, timezone
from inventory.models import LoanerInventoryItem, RepairInventoryItem
from organizations.models import Organization
from slas.models import SLA

from .upload_content import UploadContent

DELIVERED_STATUS_VALUES = ["Delivered"]
CLOSED_STATUS_VALUES = ["Ready", "Ready For Pickup"]


class TicketManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super(TicketManager, self).__init__(*args, **kwargs)
        self.alive_only = True

    def get_queryset(self):
        return TicketQuerySet(self.model).filter(is_deleted=False)


class TicketQuerySet(BaseQuerySet):
    def delete(self):
        super(TicketQuerySet, self).update(reference_number=None)
        return super(TicketQuerySet, self).delete()

    def open(self):
        return self.exclude(status__in=DELIVERED_STATUS_VALUES)

    def due_between(self, **kwargs):
        dt = timezone.now()
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), dt.tzinfo)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.open().filter(expected_delivery_time__lt=end_time)

    def closed_between(self, **kwargs):
        dt = timezone.now()
        mid_night_today = datetime.combine(dt.date(), datetime.min.time(), dt.tzinfo)
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), dt.tzinfo)
        start_time = kwargs.get("start_time", mid_night_today)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.filter(closed_on__range=[start_time, end_time])

    def first_level_escalations(self, **kwargs):
        dt = timezone.now()
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), dt.tzinfo)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.open().filter(final_escalation_after__lt=end_time)

    def second_level_escalations(self, **kwargs):
        dt = timezone.now()
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), dt.tzinfo)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.open().filter(second_escalation_after__lt=end_time)

    def final_level_escalations(self, **kwargs):
        dt = timezone.now()
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), dt.tzinfo)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.open().filter(final_escalation_after__lt=end_time)


class Ticket(BaseModel):
    organization = models.ForeignKey(
        Organization, related_name="tickets", on_delete=models.DO_NOTHING
    )
    device = models.OneToOneField(
        Device, related_name="ticket", on_delete=models.DO_NOTHING
    )
    customer = models.OneToOneField(
        Customer, related_name="ticket", on_delete=models.DO_NOTHING
    )
    password = models.CharField(max_length=100, default="NA", null=True)
    initial_operating_system = models.CharField(max_length=100, default="NA", null=True)
    repair_classification = models.CharField(max_length=100, default="SINGLE")
    gsx_coverage_option = models.CharField(max_length=100, default="BATTERY")
    request_review_by_apple = models.BooleanField(default=False)
    mark_complete = models.BooleanField(default=False)
    box_required = models.BooleanField(default=False)
    loaner_stock_unavailable = models.BooleanField(default=False)
    currently_assigned_to = models.ForeignKey(
        User, related_name="assigned_tickets", on_delete=models.DO_NOTHING
    )
    status = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    repair_type = models.CharField(max_length=100)
    issue_reported_by_customer = models.CharField(max_length=500)
    device_condition = models.CharField(max_length=500)
    expected_service_cost = models.FloatField(default=0.0)
    expected_hardware_cost = models.FloatField(default=0.0)
    accessories = models.CharField(default="NA", max_length=500)
    required_upgrades = models.TextField(default="NA", max_length=500)
    expected_delivery_time = models.DateTimeField()
    is_backup_required = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=50, unique=True)
    is_standby_device_required = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(
        User, related_name="subscribed_tickets", blank=True
    )
    first_escalation_after = models.DateTimeField()
    second_escalation_after = models.DateTimeField()
    final_escalation_after = models.DateTimeField()
    closed_on = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(
        User, null=True, related_name="closed_tickets", on_delete=models.DO_NOTHING
    )
    orderlines = models.ManyToManyField(
        RepairInventoryItem,
        through="OrderLine",
        through_fields=("ticket", "inventory_item"),
    )
    loaner_devices = models.ManyToManyField(
        LoanerInventoryItem,
        through="LoanerRecord",
        through_fields=("ticket", "inventory_item"),
    )

    sla = models.ForeignKey(
        SLA, null=False, related_name="tickets", on_delete=models.DO_NOTHING
    )
    uploaded_contents = GenericRelation(UploadContent, related_query_name="tickets")
    customer_signature = models.ImageField(
        upload_to="customer_signatures/tickets", null=True, blank=True
    )
    unit_part_reports = JSONField(null=True)
    component_issues = JSONField(null=True)
    objects = TicketManager()
    all_objects = TicketManager(alive_only=False)

    class Meta:
        "Ticket Model Meta"
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-id"]

    @property
    def expected_time_to_delivery(self):
        return self.expected_delivery_time - self.created_at

    @property
    def expected_cost(self):
        return self.expected_hardware_cost + self.expected_service_cost

    @property
    def actual_cost(self):
        d = self.delivery
        return d.actual_hardware_cost + d.actual_service_cost

    @property
    def is_closed(self):
        return self.status is CLOSED_STATUS_VALUES

    @property
    def is_delivered(self):
        return self.status in DELIVERED_STATUS_VALUES

    def has_consolidated_loaner_items(self):
        flag = True
        for i in self.loaner_records.all():
            if not i.is_returned:
                flag = False
        return flag

    def has_consolidated_order_lines(self):
        return (
            self.order_lines.all().count()
            or self.serializable_order_lines.all().count()
        )

    def has_consolidated_gsx_repair_info(self):
        return self.gsx_informations.all().count()

    @property
    def turn_around_time(self):
        return self.closing_time - self.created_at

    @property
    def delay_in_completing_job(self):
        return self.expected_delivery_time - self.closing_time

    @property
    def delay_in_delivery(self):
        return self.delivery.actual_delivery_time - self.expected_delivery_time

    def set_reference_number(self):
        code = self.organization.code
        index = self.organization.tickets.count() + 1
        suffix = settings.TICKET_SUFFIX
        reference_number = "{}{}{}{}".format(code, index, random.randint(0, 99), suffix)
        self.reference_number = reference_number

    def refresh_escalation_timestamps(self, closed=False):
        if not self.is_closed:
            self.first_escalation_after = time_by_adding_business_days(1)
            self.second_escalation_after = time_by_adding_business_days(2)
            self.final_escalation_after = time_by_adding_business_days(29)

    def send_ticket_details_to_customer_via_email(self):
        template = settings.EMAIL_TEMPLATES.get("action")
        ticket_display_url = settings.CLIENT_URL
        subject = "Device repair details for {0}".format(self)
        summary = (
            "We have received your device for repair and details are listed bellow."
        )
        message = """For further assistance you may  call on {0} between ({1})
        or you may also send your queries to {2} .""".format(
            self.organization.contact_number,
            self.organization.timings,
            self.organization.email,
        )
        action_summary = """We will take it up for diagnosis and updates will be shared
        over email & SMS"""
        table_data = {
            "RAF No.": self.reference_number,
            "Product Details.": self.device.product_name,
            "Serial Number.": self.device.serial_number,
            "Problem Reported": self.issue_reported_by_customer,
        }
        context = {
            "receiver_short_name": self.customer.full_name,
            "from_name": self.organization.name,
            "site_name": self.organization.name,
            "summary": summary,
            "detail": message,
            "action_summary": action_summary,
            "action_name": "Click here to check your repair status",
            "action_link": ticket_display_url,
            "sender_full_name": "Team {0}".format(self.organization.name),
            "table_data": table_data,
        }
        receivers = [self.customer.email]
        utils.send_mail(subject, template, *receivers, **context)
        return receivers

    def send_ticket_details_to_customer_via_sms(self):
        message = """Thank you for visiting {0}.Your Ticket No is {1} visit {2} to track status.Updates will be sent on SMS and Email.""".format(
            self.organization.name.split(" ")[0], self, settings.CLIENT_URL
        )

        send_sms_res = send_sms(self.customer.contact_number, message)
        return send_sms_res

    def get_invite_message_by_status(self):
        if self.status.lower() in ["Ready For Pickup".lower()]:
            return "Device ready for delivery. Timings {}.".format(
                self.organization.timings
            )
        return "Ticket status changed to {}. Timings {} Call {} for your query.".format(
            self.status, self.organization.timings, self.organization.contact_number
        )

    def send_ticket_status_update_to_customer_via_sms(self):
        message = """{0} update for Ticket No {1}. {2}""".format(
            self.organization.name.split(" ")[0],
            self,
            self.get_invite_message_by_status(),
        )
        send_sms_res = send_sms(self.customer.contact_number, message)

        return send_sms_res

    def send_ticket_status_update_to_customer_via_email(self):
        template = settings.EMAIL_TEMPLATES.get("action")
        ticket_display_url = settings.CLIENT_URL

        subject = "{0} update for Ticket No {1}".format(
            self.organization.name.split(" ")[0], self
        )
        message = """{0} update for Ticket No {1}.
        {2}""".format(
            self.organization.name.split(" ")[0],
            self,
            self.get_invite_message_by_status(),
        )

        action_summary = """Any other updates will be shared
        over email & SMS"""
        table_data = {
            "RAF No.": self.reference_number,
            "Product Details.": self.device.product_name,
            "Serial Number.": self.device.serial_number,
            "Problem Reported": self.issue_reported_by_customer,
            "Current Status": self.status,
        }

        context = {
            "receiver_short_name": self.customer.full_name,
            "from_name": self.organization.name,
            "site_name": self.organization.name,
            "detail": message,
            "action_summary": action_summary,
            "action_name": "Click here to check your repair status",
            "action_link": ticket_display_url,
            "sender_full_name": "Team {0}".format(self.organization.name),
            "table_data": table_data,
        }

        receivers = [self.customer.email]
        utils.send_mail(subject, template, *receivers, **context)
        return receivers

    def __str__(self):
        return self.reference_number


@receiver(pre_save, sender=Ticket)
def set_reference_number_for_ticket(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        instance.set_reference_number()
    if not instance.id:
        instance.refresh_escalation_timestamps()
