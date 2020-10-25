# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from slas import viewsets

sla_router = DefaultRouter()
sla_router.register(r"slas", viewsets.SLAViewSet)
sla_router.register(r"terms", viewsets.TermViewSet)
