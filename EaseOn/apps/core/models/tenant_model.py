# -*- coding: utf-8 -*-
from core.utils import get_organization_model
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class TenantMixin(object):
    def set_organization(self, value):
        self.organization = value

    def get_organization(self):
        return self.organization


class BaseTenantModel(models.Model):
    organization = models.ForeignKey(
        get_organization_model(),
        related_name='%(class)s',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
