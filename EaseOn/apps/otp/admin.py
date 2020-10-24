#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
- otp.admin
~~~~~~~~~~~~~~

- This file contains admin models of pyotp app
"""

# future
from __future__ import unicode_literals

# Django
from django.contrib import admin

# own app
from otp import models

# 3rd party

# local


class PyOTPAdmin(admin.ModelAdmin):
    """"""

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
