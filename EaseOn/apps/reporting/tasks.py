# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from core.utils import get_organization_model
from django.apps import apps

from celery import shared_task


@shared_task
def send_a_report(
    organization_id, report_type, start_date, end_date, *receivers
):
    """
    Task To Run On New Report Request
    """
    organization_modal = apps.get_model(
        *get_organization_model().split('.', 1)
    )
    organization = organization_modal.objects.get(pk=organization_id)
    organization.send_report_by_mail(
        report_type, start_date, end_date, *receivers
    )
