# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.admin import register
from django.contrib import admin
from organizations.models import Organization

from .import_resources import OrganizationResourceAdmin

register(Organization, OrganizationResourceAdmin)
