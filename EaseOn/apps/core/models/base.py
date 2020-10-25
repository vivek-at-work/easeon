# -*- coding: utf-8 -*-
import hashlib
import random

from django.db import models
from django.utils import timezone

from .querysets import BaseManager
from .user import User


class BaseModel(models.Model):
    """
    Base Model for all django models in EaseOn App
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    guid = models.CharField(max_length=40, editable=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User,
        related_name="created_%(class)s",
        editable=False,
        on_delete=models.DO_NOTHING,
    )
    last_modified_by = models.ForeignKey(
        User, null=True, related_name="modified_%(class)s", on_delete=models.DO_NOTHING
    )
    version = models.CharField(default="v0", max_length=3)
    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta:
        get_latest_by = "created_at"
        ordering = ("-updated_at", "-created_at")
        abstract = True

    def _increment_version(self):
        current_object_version = self.version
        preposed_object_version = current_object_version[0] + str(
            int(current_object_version[1:]) + 1
        )
        self.version = preposed_object_version

    @property
    def is_alive(self):
        return not (self.is_deleted and self.deleted_at is not None)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        return super(BaseModel, self).delete()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random()).encode("utf-8")).hexdigest()
        self._increment_version()
        return super(BaseModel, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
