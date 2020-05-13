# -*- coding: utf-8 -*-
import django_filters
from core.filters import FullNameFilter
from core.permissions import OPERATOR, SUPER_USER
from core.utils import PageNumberPagination
from core.viewsets import BaseViewSet
from django.contrib.auth import get_user_model
from organizations import models, serializers
from rest_framework import decorators, permissions, response, status


class OrganizationPermissions(permissions.BasePermission):

    READ_ROLES = [SUPER_USER, OPERATOR]
    CREATE_DELETE_ROLES = [SUPER_USER]
    UPDATE_ROLES = [OPERATOR, SUPER_USER]

    def has_permission(self, request, view):
        if (
            view.action in ['list', 'get_holidays']
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.READ_ROLES
        ):
            return True

        if (
            view.action in ['create', 'destroy']
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.CREATE_DELETE_ROLES
        ):
            return True
        if (
            view.action
            in [
                'retrieve',
                'update',
                'partial_update',
                'destroy',
                'add_holiday',
            ]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.UPDATE_ROLES
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER:
            return True

        if (
            view.action in ['create', 'destroy']
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.CREATE_DELETE_ROLES
        ):
            return request.user.role == SUPER_USER

        if (
            view.action
            in [
                'retrieve',
                'update',
                'partial_update',
                'destroy',
                'add_holiday',
            ]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.UPDATE_ROLES
        ):
            return (
                request.user.role == SUPER_USER or request.user == obj.manager
            )


class OrganizationFilter(django_filters.FilterSet):
    manager = django_filters.CharFilter(
        field_name='manager__username', lookup_expr='icontains'
    )
    manager_name = FullNameFilter(field_name='manager')
    users = django_filters.ModelMultipleChoiceFilter(
        queryset=get_user_model().objects.all()
    )
    email = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    contact_number = django_filters.CharFilter(lookup_expr='icontains')
    created_at_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )
    created_at_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )

    class Meta(object):
        model = models.Organization
        fields = ['name', 'code', 'token_machine_location_code', 'gsx_ship_to']


class OrganizationViewSet(BaseViewSet):
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (OrganizationPermissions,)
    search_fields = ('name', 'email', 'code')
    filter_class = OrganizationFilter

    def get_queryset(self):
        model = models.Organization
        return model.objects.all()

    @decorators.action(
        methods=['POST'],
        detail=True,
        serializer_class=serializers.HolidaySerializer,
    )
    def add_holiday(self, request, pk=None):
        'Get diagnosis suites for device.'
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(
            serializer.errors, status.HTTP_400_BAD_REQUEST
        )

    @decorators.action(
        methods=['GET'],
        detail=True,
        serializer_class=serializers.HolidaySerializer,
    )
    def get_holidays(self, request, pk=None):
        'Get diagnosis suites for device.'
        organization = self.get_object()
        serializer = self.serializer_class(
            organization.holidays.all(),
            many=True,
            context={'request': request},
        )
        return response.Response(serializer.data)
