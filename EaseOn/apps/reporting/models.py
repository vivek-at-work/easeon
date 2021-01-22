# -*- coding: utf-8 -*-
import os

from core import utils
from core.models import BaseModel, User
from django.conf import settings
from django.db import connection, models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .tasks import process_report_request


class ReportRequest(BaseModel):
    organization = models.ForeignKey(
        utils.get_organization_model(),
        on_delete=models.DO_NOTHING,
        related_name="requested_reports",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    report_type = models.CharField(max_length=50)
    report_path = models.CharField(max_length=200)

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

    @property
    def final_report_path(self):
        return os.path.join(settings.REPORTS_DIR, self.report_path)

    @property
    def is_processed(self):
        return os.path.exists(self.final_report_path)

    def process_async(self):
        process_report_request.delay(
            self.organization.id,
            self.final_report_path,
            self.report_type,
            self.start_date,
            self.end_date,
            self.created_by.email,
        )

    def process(self):
        process_report_request(
            self.organization.id,
            self.final_report_path,
            self.report_type,
            self.start_date,
            self.end_date,
            self.created_by.email,
        )


@receiver(post_save, sender=ReportRequest)
def process_request(sender, instance, created, **kwargs):
    instance.process_async()
