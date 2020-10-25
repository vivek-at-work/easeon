# -*- coding: utf-8 -*-
"""Service Provider API View Sets"""
import django_filters
from core.permissions import OPERATOR, SUPER_USER
from core.viewsets import BaseViewSet
from organizations.models import Organization, OrganizationRights
from organizations.serializers import OrganizationRightsSerializer
from rest_framework import decorators, permissions, response


class MemershipPermissions(permissions.BasePermission):

    READ_ROLES = [SUPER_USER, OPERATOR]
    CREATE_ROLES = [SUPER_USER, OPERATOR]
    UPDATE_ROLES = [SUPER_USER]
    DESTROY_ROLES = [SUPER_USER]

    def has_permission(self, request, view):
        if (
            view.action == "list"
            and request.user
            and request.user.is_authenticated
            and request.user.role not in self.READ_ROLES
        ):
            return True

        if (
            view.action in ["create"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.CREATE_ROLES
        ):
            return True

        if (
            view.action
            in ["retrieve", "update", "partial_update", "activate", "deactivate"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.UPDATE_ROLES
        ):
            return True

        if (
            view.action in ["destroy"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.DESTROY_ROLES
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER:
            return True

        if (
            view.action in ["create"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.CREATE_ROLES
        ):
            return request.user.role in self.CREATE_ROLES

        if (
            view.action
            in ["retrieve", "update", "partial_update", "activate", "deactivate"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.UPDATE_ROLES
        ):
            return request.user.role == SUPER_USER or request.user == obj.manager

        if (
            view.action in ["destroy"]
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.DESTROY_ROLES
        ):
            return True
        return False


class MembershipFilter(django_filters.FilterSet):
    """Membership Filter"""

    user = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    organizations = django_filters.ModelMultipleChoiceFilter(
        field_name="organization_id", queryset=Organization.objects.all()
    )

    class Meta(object):
        model = OrganizationRights
        fields = []


class MembershipViewSet(BaseViewSet):
    "Membership View Set"
    serializer_class = OrganizationRightsSerializer
    permission_classes = [MemershipPermissions]
    filter_class = MembershipFilter

    def get_queryset(self):
        model = OrganizationRights
        return model.objects.all()

    @decorators.action(methods=["post"], detail=True)
    def activate(self, request, pk=None):
        membership = self.get_object()
        membership.toggle_activation(True)
        context = {"request": request}
        return response.Response(
            self.serializer_class(membership, context=context).data
        )

    @decorators.action(methods=["post"], detail=True)
    def deactivate(self, request, pk=None):
        membership = self.get_object()
        membership.toggle_activation(False)
        context = {"request": request}
        return response.Response(
            self.serializer_class(membership, context=context).data
        )
