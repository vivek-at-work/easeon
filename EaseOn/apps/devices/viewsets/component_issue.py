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


class ComponenetIssueViewSet(BaseViewSet):
    serializer_class = serializers.ComponentIssueSerializer
    queryset = models.ComponentIssue.objects.all()
