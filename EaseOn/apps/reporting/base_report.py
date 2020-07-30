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
        if type(date_text)==datetime.date:
            datetime.datetime.strftime(date_text, "%Y-%m-%d")
        else:
            datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return True
    
class BaseReportTarget():
    def send(self):
        raise NotImplementedError

class SMTPReportTarget(BaseReportTarget):

    def send(self,subject,report,*receivers):
        from core.utils import send_mail
        template = settings.EMAIL_TEMPLATES.get('alert', None)
        summary = """Please find attached report."""
        details = (
            'Please Delete this mail if you received it by mistake.'
        )
        context = {
            'receiver_short_name': "All",
            'summary': summary,
            'detail': details,
            'files':[report.target_path]
        }
        send_mail(subject, template, *receivers, **context)


class Report():
    def __init__(self,report_type,db_query,file_name=None):
        if not os.path.exists(settings.REPORTS_DIR):
            os.mkdir(settings.REPORTS_DIR)
        self.report_type=report_type
        self.db_query = db_query
        self.target_path = self._get_target_file_path(file_name)
          
    def _create_target_directory(self):
        target_dir = os.path.join(settings.REPORTS_DIR, self.report_type.lower())
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        return target_dir

    def _get_target_file_path(self,file_name=None):
        target_dir = self._create_target_directory()
        if file_name:
            if not file_name.endswith('.csv'):
                file_name = "{}.csv".format(file_name)
        else:
            file_name = file_name = "{}.csv".format(str(uuid.uuid4()))
        return os.path.join(target_dir,file_name)

    def create(self):
        db_cursor = connection.cursor()
        query = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(self.db_query)
        with open(self.target_path, 'w') as f_output:
            db_cursor.copy_expert(query, f_output)

    def send(self,report_target):
        self._fetch_data()
        report_target.send(self.target_path)
