# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from organizations.viewsets import (HolidayViewSet, MembershipViewSet,
                                    OrganizationViewSet)

organizations_router = DefaultRouter()
organizations_router.register(
    r'organizations', OrganizationViewSet, basename='organization'
)
organizations_router.register(
    r'rights', MembershipViewSet, basename='organizationrights'
)
organizations_router.register(r'holidays', HolidayViewSet, basename='holiday')
