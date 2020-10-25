# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.utils import time_by_adding_business_days, get_organization_model
from django.apps import apps
from reporting import (
    StatusReport,
    SMTPReportTarget,
    LoanerRecordReport,
    OrderLineReport,
    DeliveryReport,
)


def create_status_report(organization, file_name, start_date, end_date):
    status_report = StatusReport(file_name=file_name)
    if start_date is not None:
        status_report.filter_by_centre_and_date(
            organization.id, start_date, end_date
        )
    status_report.create()
    return (
        status_report,
        f"Status Report with Customer Data for {organization.code}",
    )


def create_delivery_report(organization, file_name, start_date, end_date):
    status_report = DeliveryReport(file_name=file_name)
    if start_date is not None:
        status_report.filter_by_centre_and_date(
            organization.id, start_date, end_date
        )
    status_report.create()
    return (
        status_report,
        f"Delivery Report with Customer Data for {organization.code}",
    )


def create_loaner_record_report(organization, file_name, start_date, end_date):
    loaner_record_report = LoanerRecordReport(file_name=file_name)
    if start_date is not None:
        loaner_record_report.filter_by_centre_and_date(
            organization.id, date_text, start_date, end_date
        )
    loaner_record_report.create()
    return (
        loaner_record_report,
        f"Loaner Record Report for {organization.code}",
    )


def create_order_line_report(organization, file_name, start_date, end_date):
    loaner_record_report = OrderLineReport(file_name=file_name)
    if start_date is not None:
        loaner_record_report.filter_by_centre_and_date(
            organization.id, start_date, end_date
        )
    loaner_record_report.create()
    return loaner_record_report, f"Order Line Report for {organization.code}"


REPORT_GENRATORS = {
    'create_status_report': create_status_report,
    'create_loaner_record_report': create_loaner_record_report,
    'create_order_line_report': create_order_line_report,
    'create_delivery_report': create_delivery_report,
}


def create_report(
    organization, file_name, report_type, start_date, end_date, *receivers
):
    report, subject = REPORT_GENRATORS.get(f'create_{report_type.lower()}')(
        organization,
        file_name,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
    )


@shared_task
def process_report_request(
    organization_id, file_name, report_type, start_date, end_date, *receivers
):
    """
    Task To Run On New Report Request
    """
    organization_modal = apps.get_model(
        *get_organization_model().split('.', 1)
    )
    organization = organization_modal.objects.get(pk=organization_id)
    create_report(
        organization, file_name, report_type, start_date, end_date, *receivers
    )
