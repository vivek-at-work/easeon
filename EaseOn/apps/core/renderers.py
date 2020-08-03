# -*- coding: utf-8 -*-
import datetime
import json

import pytz
from django.conf import settings
from rest_framework.renderers import (
    BaseRenderer,
    BrowsableAPIRenderer,
    JSONRenderer,
)
from rest_framework.utils import encoders


class BrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        parent = super(BrowsableAPIRenderer, self)
        context = parent.get_context(
            data, accepted_media_type, renderer_context
        )
        context['SITE_HEADER'] = settings.SITE_HEADER
        return context


class JSONEncoder(encoders.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            obj = obj.astimezone(pytz.utc)
        return super(JSONEncoder, self).default(obj)


class JSONRenderer(JSONRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        parent = super(BrowsableAPIRenderer, self)
        context = parent.get_context(
            data, accepted_media_type, renderer_context
        )
        context['SITE_HEADER'] = settings.SITE_HEADER
        return context
