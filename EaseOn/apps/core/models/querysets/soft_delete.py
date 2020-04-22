# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(
            deleted_at=timezone.now(), is_deleted=True
        )

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.exclude(is_deleted=False)

    def rollback(self):
        return super(SoftDeletionQuerySet, self).update(
            deleted_at=None, is_deleted=False
        )
