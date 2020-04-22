# -*- coding: utf-8 -*-
from core.models import BaseManager, BaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

UPLOAD_TYPES = (('Ticket', 'Ticket'), ('Delivery', 'Delivery'))


class UploadContent(BaseModel):
    file = models.FileField(blank=False, null=False)
    upload_type = models.CharField(max_length=255, choices=UPLOAD_TYPES)
    description = models.CharField(max_length=255)
    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)
