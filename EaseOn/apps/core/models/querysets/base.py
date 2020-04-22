# -*- coding: utf-8 -*-
from django.db import models

from .soft_delete import SoftDeletionQuerySet
from .timestamped_query_set import TimeStampedQuerySet


class BaseQuerySet(SoftDeletionQuerySet, TimeStampedQuerySet):
    pass


class BaseManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        alive_only = kwargs.pop('alive_only', None)
        super(BaseManager, self).__init__(*args, **kwargs)
        self.alive_only = alive_only

    def get_queryset(self):
        if self.alive_only is None:
            return BaseQuerySet(self.model).filter(is_deleted=False)
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
