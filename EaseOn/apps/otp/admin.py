# -*- coding: utf-8 -*-
from django.contrib import admin
from otp import models


class PyOTPAdmin(admin.ModelAdmin):
    """
    """

    list_display = (
        'id',
        'uuid',
        'secret',
        'count',
        'interval',
        'otp',
        'created_at',
    )
    list_display_links = ('uuid',)
    search_fields = ('uuid', 'secret', 'otp')
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(models.PyOTP, PyOTPAdmin)
