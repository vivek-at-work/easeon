# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        if self.created_at is not None:
            return now() - self.created_at
        return None

    @property
    def time_since_last_update(self):
        if self.created_at is not None:
            return now() - self.updated_at
        return None

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-updated_at', '-created_at')
        abstract = True
