# -*- coding: utf-8 -*-
import logging

import django_filters
from core.permissions import HasManagerRightsToUpdateOrDelete
from core.viewsets import BaseViewSet
from devices import models, serializers
from devices.exceptions import DeviceDetailsExceptions
from django.conf import settings
from django.db.models import Q
from rest_framework import decorators, generics, permissions, response, status, views


class DeviceFilter(django_filters.FilterSet):
    """Device Filter"""

    serial_number = django_filters.CharFilter(lookup_expr="icontains")
    alternate_device_id = django_filters.CharFilter(lookup_expr="icontains")
    product_name = django_filters.CharFilter(lookup_expr="icontains")
    configuration = django_filters.CharFilter(lookup_expr="icontains")

    class Meta(object):
        model = models.Device
        exclude = ()


class DeviceViewSet(BaseViewSet):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    queryset = models.Device.objects.all()
    filter_class = DeviceFilter
