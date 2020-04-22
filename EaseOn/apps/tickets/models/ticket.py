# -*- coding: utf-8 -*-
"""
Ticket Models
"""
from datetime import date, datetime, time

from core.gsx import GSXRequest, format_customer, format_device
from core.models import BaseManager, BaseModel, BaseQuerySet, User
from core.utils import get_random_string, time_by_adding_business_days
from customers.models import Customer
from devices.models import Device
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from inventory.models import LoanerInventoryItem, RepairInventoryItem
from organizations.models import Organization
from slas.models import SLA

from .upload_content import UploadContent

CLOSE_STATUS_VALUES = ['Delivered', 'Hold', 'DECLINED']


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
        return self.filter(closed_on__isnull=True, is_deleted=False)

    def due_between(self, **kwargs):
        dt = timezone.now()
        mid_night_tomorrow = datetime.combine(
            dt.date(), datetime.max.time(), dt.tzinfo
        )
        end_time = kwargs.get('end_time', mid_night_tomorrow)
        return self.filter(
            closed_on__isnull=True,
            is_deleted=False,
            expected_delivery_time__lt=end_time,
        )

    def closed_between(self, **kwargs):
        dt = timezone.now()
        mid_night_today = datetime.combine(
            dt.date(), datetime.min.time(), dt.tzinfo
        )
        mid_night_tomorrow = datetime.combine(
            dt.date(), datetime.max.time(), dt.tzinfo
        )
        start_time = kwargs.get('start_time', mid_night_today)
        end_time = kwargs.get('end_time', mid_night_tomorrow)
        return self.filter(closed_on__range=[start_time, end_time])


class Ticket(BaseModel):
    organization = models.ForeignKey(
        Organization, related_name='tickets', on_delete=models.DO_NOTHING
    )
    device = models.ForeignKey(
        Device, related_name='tickets', on_delete=models.DO_NOTHING
    )
    customer = models.ForeignKey(
        Customer, related_name='tickets', on_delete=models.DO_NOTHING
    )
    password = models.CharField(max_length=100, default='NA', null=True)
    initial_operating_system = models.CharField(
        max_length=100, default='NA', null=True
    )
    currently_assigned_to = models.ForeignKey(
        User, related_name='assigned_tickets', on_delete=models.DO_NOTHING
    )
    status = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    # gsx_service_type = models.CharField(max_length=100)
    repair_type = models.CharField(max_length=100)
    issue_reported_by_customer = models.CharField(max_length=500)
    device_condition = models.CharField(max_length=500)
    expected_service_cost = models.FloatField(default=0.0)
    expected_hardware_cost = models.FloatField(default=0.0)
    accessories = models.CharField(default='NA', max_length=500)
    required_upgrades = models.TextField(default='NA', max_length=500)
    expected_delivery_time = models.DateTimeField()
    is_backup_required = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=50, unique=True)
    is_standby_device_required = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(
        User, related_name='subscribed_tickets', blank=True
    )
    first_escalation_after = models.DateTimeField()
    second_escalation_after = models.DateTimeField()
    final_escalation_after = models.DateTimeField()
    closed_on = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(
        User,
        null=True,
        related_name='closed_tickets',
        on_delete=models.DO_NOTHING,
    )
    orderlines = models.ManyToManyField(
        RepairInventoryItem,
        through='OrderLine',
        through_fields=('ticket', 'inventory_item'),
    )
    loaner_devices = models.ManyToManyField(
        LoanerInventoryItem,
        through='LoanerRecord',
        through_fields=('ticket', 'inventory_item'),
    )

    sla = models.ForeignKey(
        SLA, null=False, related_name='tickets', on_delete=models.DO_NOTHING
    )
    uploaded_contents = GenericRelation(
        UploadContent, related_query_name='tickets'
    )
    objects = TicketManager()
    all_objects = TicketManager(alive_only=False)

    class Meta:
        'Ticket Model Meta'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

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
        return self.status in CLOSE_STATUS_VALUES

    def can_be_closed(self):
        return self.status in CLOSE_STATUS_VALUES

    def has_consolidated_loaner_items(self, obj):
        flag = True
        for i in self.loaner_records:
            if not i.is_returned:
                flag = False
        return flag

    def has_consolidated_order_lines(self, obj):
        return (
            self.order_lines.all().count()
            or self.serializable_order_lines.all().count()
        )

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
        reference_number = '{0}{1}{2}'.format(code, index, suffix)
        self.reference_number = reference_number

    def refresh_escalation_timestamps(self, closed=False):
        if not closed:
            self.first_escalation_after = time_by_adding_business_days(1)
            self.second_escalation_after = time_by_adding_business_days(2)
            self.final_escalation_after = time_by_adding_business_days(3)
        else:
            self.first_escalation_after = None
            self.second_escalation_after = None
            self.final_escalation_after = None

    def __str__(self):
        return self.reference_number


@receiver(pre_save, sender=Ticket)
def set_reference_number_for_ticket(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        instance.set_reference_number()
    instance.refresh_escalation_timestamps()


@receiver(pre_save, sender=Ticket)
def set_closed_on(sender, instance, *args, **kwargs):
    if not instance.closed_on and instance.can_be_closed():
        instance.closed_on = timezone.now()
        instance.closed_by = instance.last_modified_by
        instance.refresh_escalation_timestamps(closed=True)


# @receiver(post_save, sender=Ticket)
# def add_subscribers(sender, instance, *args, **kwargs):
#     subscribers = [
#         instance.currently_assigned_to,
#         instance.created_by,
#         instance.organization.manager,
#     ]
