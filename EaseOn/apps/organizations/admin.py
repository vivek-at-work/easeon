# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.admin import register
from organizations.models import Organization
from django.contrib import admin
from .import_resources import OrganizationResourceAdmin


register(Organization, OrganizationResourceAdmin)
