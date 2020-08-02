# -*- coding: utf-8 -*-
from core import utils
from core.models import BaseModel, User
from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .tasks import send_a_report


class ReportRequest(BaseModel):
    organization = models.ForeignKey(
        utils.get_organization_model(),
        on_delete=models.DO_NOTHING,
        related_name='requested_reports',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    report_type = models.CharField(max_length=50)
    is_processed = models.BooleanField(default=False)

    def process(self):
        send_a_report.delay(
            self.organization.id,
            self.report_type,
            self.start_date,
            self.end_date,
            self.created_by.email,
        )


@receiver(post_save, sender=ReportRequest)
def process_request(sender, instance, created, **kwargs):
    instance.process()
