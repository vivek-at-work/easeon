# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseViewSet
from devices import models, serializers
from django.conf import settings
from django.db.models import Q
import logging
from rest_framework import (
    decorators,
    generics,
    permissions,
    response,
    status,
    views,
)
from devices.exceptions import DeviceDetailsExceptions


class DeviceFilter(django_filters.FilterSet):
    """Device Filter"""

    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    alternate_device_id = django_filters.CharFilter(lookup_expr='icontains')
    product_name = django_filters.CharFilter(lookup_expr='icontains')
    configuration = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = models.Device
        exclude = ()


class DeviceViewSet(BaseViewSet):
    serializer_class = serializers.DeviceSerializer
    queryset = models.Device.objects.all()
    filter_class = DeviceFilter

    @decorators.action(methods=['GET'], detail=True)
    def warranty(self, request, pk=None):
        'Get warranty for device.'
        if pk is not None:
            device = self.get_object()
            data = device.get_warranty(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
        return response.Response(data)

    @decorators.action(methods=['GET'], detail=True)
    def component_issue(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            suites = device.get_component_issue(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(suites)

    @decorators.action(methods=['GET'], detail=True)
    def questions(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            questions = device.get_repair_questions(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(questions)

    @decorators.action(methods=['GET'], detail=True)
    def get_parts(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            questions = device.get_parts(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(questions)

    @decorators.action(methods=['GET'], detail=False)
    def diagnosis_suites(self, request, pk=None):
        'Get diagnosis suites for device.'
        sn = request.query_params['sn']
        device = models.Device.objects.filter(
            Q(serial_number=sn) | Q(alternate_device_id=sn)
        ).first()
        suites = device.get_diagnostic_suites(
            request.user.gsx_user_name, request.user.gsx_auth_token
        )
        return response.Response(suites)

    @decorators.action(methods=['post', 'GET'], detail=True)
    def run_diagnosis_suite(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            suiteId = request.data.get('suiteId')
            result = device.run_diagnosis_suite(
                suiteId,
                request.user.gsx_user_name,
                request.user.gsx_auth_token,
            )
            return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['GET'], detail=False)
    def run_diagnosis_suite_via_sn(self, request, pk=None):
        'Get diagnosis suites for device.'
        from django.db.models import Q

        sn = request.query_params['sn']
        suiteId = request.query_params['suiteId']
        device = models.Device.objects.filter(
            Q(serial_number=sn) | Q(alternate_device_id=sn)
        ).first()
        result = device.run_diagnosis_suite(
            suiteId, request.user.gsx_user_name, request.user.gsx_auth_token
        )
        return response.Response(result)

    @decorators.action(methods=['post', 'GET'], detail=True)
    def diagnosis_lookup(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            result = device.fetch_diagnosis_lookup(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'GET'], detail=False)
    def diagnosis_lookup_via_sn(self, request, pk=None):
        'Get diagnosis suites for device.'
        from django.db.models import Q

        sn = request.query_params['sn']
        device = models.Device.objects.filter(
            Q(serial_number=sn) | Q(alternate_device_id=sn)
        ).first()
        result = device.fetch_diagnosis_lookup(
            request.user.gsx_user_name, request.user.gsx_auth_token
        )
        diagnostics = result['diagnostics']
        largest = {}
        if diagnostics:
            largest = diagnostics[0]
            for diagnostic in diagnostics:
                if (
                    float(largest['context']['diagnosticEventNumber'])
                ) < float(diagnostic['context']['diagnosticEventNumber']):
                    largest = diagnostic

        return response.Response(largest)

    @decorators.action(methods=['post', 'GET'], detail=True)
    def fetch_diagnosis_console_url(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            eventNumber = request.data.get('eventNumber')
            token = request.user.gsx_auth_token
            result = device.fetch_diagnosis_console_url(
                eventNumber, request.user.gsx_user_name, token
            )
            return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['GET'], detail=True)
    def get_repair_eligibility(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            eligibility = device.get_repair_eligibility(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(eligibility)

    @decorators.action(methods=['GET'], detail=True)
    def previous_gsx_repairs(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            eligibility = device.get_previous_gsx_repairs(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(eligibility)

    @decorators.action(methods=['GET'], detail=True)
    def submit_consignment_order(self, request, pk=None):
        'Get diagnosis suites for device.'
        if pk is not None:
            device = self.get_object()
            eligibility = device.submit_consignment_order(
                request.user.gsx_user_name, request.user.gsx_auth_token
            )
            return response.Response(eligibility)


@decorators.api_view(['GET', 'POST'])
def run_dignosis_suits(request):
    from django.db.models import Q

    sn = request.data['sn']
    suiteId = request.data['suiteId']
    device = models.Device.objects.filter(
        Q(serial_number=sn) | Q(alternate_device_id=sn)
    ).first()
    suites = device.run_diagnosis_suite(
        suiteId, request.user.gsx_user_name, request.user.gsx_auth_token
    )
    return response.Response(suites)


@decorators.api_view(['GET', 'POST'])
def fetch_diagnosis_results(request):
    from django.db.models import Q

    sn = request.data['sn']
    device = models.Device.objects.filter(
        Q(serial_number=sn) | Q(alternate_device_id=sn)
    ).first()
    suites = device.fetch_diagnosis_lookup(
        request.user.gsx_user_name, request.user.gsx_auth_token
    )
    return response.Response(suites)
