"""
Base Report
"""
import os
import uuid
import datetime
from django.db import connection
from django.conf import settings


def validate_date(date_text):
    """
    Dates should be in YYYY-MM-DD format
    """
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return True


class BaseReportTarget:
    def send(self):
        raise NotImplementedError


class SMTPReportTarget(BaseReportTarget):
    def send(self, subject, report, *receivers):
        from core.utils import send_mail

        template = settings.EMAIL_TEMPLATES.get('alert', None)
        summary = """Please find attached report."""
        details = 'Please Delete this mail if you received it by mistake.'
        context = {
            'receiver_short_name': "All",
            'summary': summary,
            'detail': details,
            'files': [report.target_path],
        }
        send_mail(subject, template, *receivers, **context)


class Report:
    def __init__(self, report_type, db_query, file_name):
        self.report_type = report_type
        self.db_query = db_query
        self.file_name = file_name

    def create(self):
        db_cursor = connection.cursor()
        query = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(self.db_query)
        with open(self.file_name, 'w') as f_output:
            db_cursor.copy_expert(query, f_output)
