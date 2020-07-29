# -*- coding: utf-8 -*-
from rest_framework import permissions

SUPER_USER = 'SuperUser'
OPERATOR = 'Technician'
TOKEN_USER = 'TokenUser'
AUDITOR = 'Auditor'
PRIVILEGED  = 'Privileged'

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to Super users.
    """

    ALLOWED_ROLES = [SUPER_USER, PRIVILEGED]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user
            and request.user.role
            and request.user.role in self.ALLOWED_ROLES
        )


class SuperUserOrReadOnly(permissions.BasePermission):
    """
    Allows write access only to Super users.
    Does not Allows read access to Token users.
    Allows read access to Operators.
    """

    ALLOWED_ROLES = [SUPER_USER, OPERATOR,PRIVILEGED]

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            and request.user.role in self.ALLOWED_ROLES
        ):
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return IsSuperUser().has_permission(request, view)


class IsOperatorOrSuperUser(permissions.BasePermission):
    """
    Allows All access to SuperUsers and Operators .
    """

    ALLOWED_ROLES = [SUPER_USER, OPERATOR, AUDITOR,PRIVILEGED]

    def has_permission(self, request, view):
        if (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.ALLOWED_ROLES
        ):
            return True
        return False


class SuperUserOrManagerWriteOnly(IsOperatorOrSuperUser):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == SUPER_USER or request.user.role == PRIVILEGED:
            return True

        return obj.organization.manager == request.user


class IsTokenUserOrSuperUser(permissions.BasePermission):
    """
    Allows read access to All
    Write access to SuperUsers and Operators .
    """

    ALLOWED_ROLES = [SUPER_USER, TOKEN_USER,PRIVILEGED]

    def has_permission(self, request, view):
        if (
            request.method == 'GET'
            and request.user
            and request.user.is_authenticated
        ):
            return True
        if (
            request.user
            and request.user.is_authenticated
            and request.user.role not in self.ALLOWED_ROLES
        ):
            return True
        return False
