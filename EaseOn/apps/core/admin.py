# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.contrib import admin, auth
from django.utils.translation import ugettext_lazy as _


class EaseOnAdminSite(admin.AdminSite):
    site_title = _(settings.SITE_HEADER)
    site_header = _(settings.SITE_HEADER + " Administration")
    index_title = _(settings.SITE_HEADER)


class EaseOnAdminSiteConfig(admin.apps.AdminConfig):
    default_site = EaseOnAdminSite


class BaseAdmin(admin.ModelAdmin):
    exclude = (
        "created_by",
        "version",
        "last_modified_by",
        "created_at",
        "updated_at",
        "deleted_at",
        "is_deleted",
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, "created_by", None) is None:
            obj.created_by = request.user
        if getattr(obj, "created_at", None) is None:
            obj.created_at = datetime.now()
        obj.save()


def register(model, admin_model=BaseAdmin):
    BASE_SITE.register(model, admin_model)


BASE_SITE = EaseOnAdminSite()
BASE_SITE = admin.site
register(auth.get_user_model())
