# -*- coding: utf-8 -*-
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from organizations.models import Organization


class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization


class OrganizationResourceAdmin(ImportExportModelAdmin):
    list_display = ("id", "code")
    resource_class = OrganizationResource
