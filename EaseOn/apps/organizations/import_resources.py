# -*- coding: utf-8 -*-
from organizations.models import Organization
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization


class OrganizationResourceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'code')
    resource_class = OrganizationResource
