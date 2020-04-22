# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class SoftDeleteModel(models.Model):
    """
    SoftDeleteModel

    An abstract base class model that provides self-managed "is_deleted" and
    "deleted_at" fields.
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    @property
    def is_alive(self):
        return not (self.is_deleted and self.deleted_at is not None)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        return super(SoftDeleteModel, self).delete()

    class Meta:
        abstract = True
