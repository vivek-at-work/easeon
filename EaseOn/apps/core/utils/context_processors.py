# -*- coding: utf-8 -*-
def site_defaults(request):
    from django.conf import settings

    return {
        'site_name': settings.SITE_HEADER,
        'twitter_handle': settings.TWITTER_HANDLE,
    }
