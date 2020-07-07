# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from reporting.viewsets import ReportsViewSet

report_router = DefaultRouter()
report_router.register(r'reports', ReportsViewSet, basename='reportrequest')
