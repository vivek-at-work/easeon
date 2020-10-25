# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from devices.viewsets import DeviceViewSet

devices_router = DefaultRouter()
devices_router.register(r"devices", DeviceViewSet, basename="device")
