# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from core.utils import get_organization_model
from django.apps import apps

from celery import shared_task
from reporting import LOANER_RECORD_REPORT, ORDER_LINE_REPORT, STATUS_REPORT


@shared_task
def send_daily_status_reports_for_all_centres():
    organization_modal = apps.get_model(
        *get_organization_model().split('.', 1)
    )
    for organization in organization_modal.objects.all():
        organization.send_report_by_mail(STATUS_REPORT)
        organization.send_report_by_mail(LOANER_RECORD_REPORT)
        organization.send_report_by_mail(ORDER_LINE_REPORT)
