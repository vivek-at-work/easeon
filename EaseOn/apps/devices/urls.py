# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from devices.viewsets import ComponenetIssueViewSet, DeviceViewSet

devices_router = DefaultRouter()
devices_router.register(r"devices", DeviceViewSet, basename="device")
devices_router.register(
    r"component_issues", ComponenetIssueViewSet, basename="componentissue"
)
