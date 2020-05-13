# -*- coding: utf-8 -*-
""" All URLs being exposed by the API."""
from core.admin import BASE_SITE
from core.router import ROUTER
from core.urls import core_router
from core.views import (
    account_approval_from_admin_done,
    verify_email_and_request_account_approval_from_admin,
)
from customers.urls import customer_router
from devices.urls import devices_router
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from inventory.urls import inventory_router
from lists.urls import lists_router
from organizations.urls import organizations_router
from rest_framework.documentation import include_docs_urls
from slas.urls import sla_router
from tickets.urls import ticket_router
from tokens.urls import token_router
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_swagger.views import get_swagger_view

# from reports.urls import scheduler_router

API_GATEWAY = settings.ENV('API_GATEWAY')
ROUTER.extend(core_router)
ROUTER.extend(customer_router)
ROUTER.extend(devices_router)
ROUTER.extend(organizations_router)
ROUTER.extend(ticket_router)
ROUTER.extend(sla_router)
ROUTER.extend(inventory_router)
ROUTER.extend(lists_router)
ROUTER.extend(token_router)
# ROUTER.extend(scheduler_router)

schema_view = get_swagger_view(title=settings.SITE_HEADER)


urlpatterns = [
    url(r'{}/admin/'.format(API_GATEWAY), BASE_SITE.urls),
    url(
        r'backend/auth/'.format(API_GATEWAY),
        include('django.contrib.auth.urls'),
    ),
    url(
        r'{0}/{1}authentication/'.format(
            API_GATEWAY, settings.CURRENT_API_URL
        ),
        include(('core.urls', 'core'), namespace='core'),
    ),
    url(
        r'{0}/{1}gsx/'.format(API_GATEWAY, settings.CURRENT_API_URL),
        include(('gsx.urls', 'gsx'), namespace='gsx'),
    ),
    path(
        'backend/request_account_approval_from_admin/<str:uid>/<str:token>/',
        verify_email_and_request_account_approval_from_admin,
        name='request_account_approval_from_admin',
    ),
    path(
        'backend/approval_from_admin/<str:uid>/<str:token>/',
        account_approval_from_admin_done,
        name='account_approval_from_admin_done',
    ),
    url(
        r'{0}/{1}'.format(API_GATEWAY, settings.CURRENT_API_URL),
        include(ROUTER.urls),
    ),
    url(
        r'backend/api-auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
    url(
        r'backend/oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider'),
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
