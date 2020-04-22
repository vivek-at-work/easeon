# -*- coding: utf-8 -*-
import hashlib
import random
from datetime import datetime, time

from django.db import models
from django.utils import timezone

from .querysets import BaseManager
from .softdelete import SoftDeleteModel
from .tenant_model import BaseTenantModel
from .timestamp_model import TimeStampedModel
from .user import User


class BaseModel(TimeStampedModel, SoftDeleteModel):
    guid = models.CharField(max_length=40, editable=False)
    created_by = models.ForeignKey(
        User,
        related_name='created_%(class)s',
        editable=False,
        on_delete=models.DO_NOTHING,
    )
    last_modified_by = models.ForeignKey(
        User,
        null=True,
        related_name='modified_%(class)s',
        on_delete=models.DO_NOTHING,
    )
    version = models.CharField(default='v0', max_length=3)
    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta(TimeStampedModel.Meta):
        abstract = True

    def _increment_version(self):
        current_object_version = self.version
        preposed_object_version = current_object_version[0] + str(
            int(current_object_version[1:]) + 1
        )
        self.version = preposed_object_version

    def set_created_by(self, user):
        if self.created_by is None:
            self.created_by = user
        else:
            self._update_last_modified_by(user)

    def _update_last_modified_by(self, user):

        self.last_modified_by = user

    # def save(self, **kwargs):
    #     self.update_modified = kwargs.pop(
    #         'update_modified', getattr(self, 'update_modified', True)
    #     )
    #     super(TimeStampedModel, self).save(**kwargs)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.guid:
            self.guid = hashlib.sha1(
                str(random.random()).encode('utf-8')
            ).hexdigest()
        self._increment_version()
        return super(BaseModel, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )
