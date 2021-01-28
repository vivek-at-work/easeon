# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, time

from django.db import models
from django.utils import timezone


class TimeStampedQuerySet(models.QuerySet):
    def created_between(self, **kwargs):
        dt = timezone.now().astimezone(pytz.timezone('Asia/Calcutta'))
        mid_night_today = datetime.combine(dt.date(), datetime.min.time(), pytz.timezone('Asia/Calcutta'))
        mid_night_tomorrow = datetime.combine(dt.date(), datetime.max.time(), pytz.timezone('Asia/Calcutta'))
        start_time = kwargs.get("start_time", mid_night_today)
        end_time = kwargs.get("end_time", mid_night_tomorrow)
        return self.filter(created_at__range=[start_time, end_time])
