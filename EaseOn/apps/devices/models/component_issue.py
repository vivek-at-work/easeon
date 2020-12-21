# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.db import models
from .device import Device


class ComponentIssue(BaseModel):
    """A Component Issue"""

    device = models.ForeignKey(
        Device, related_name="component_issues",
        on_delete=models.CASCADE
    )
    component_code = models.CharField(max_length=100)
    component_description = models.CharField(max_length=100)
    issue_code = models.CharField(max_length=100)
    issue_description = models.CharField(max_length=100)
    reproducibility = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)
    order = models.IntegerField(default=1)
    is_technician_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Component Issue"
        verbose_name_plural = "Component Issue"
        ordering = ['-id']

    def __str__(self):
        return "{0}".format(self.componenet_code)



