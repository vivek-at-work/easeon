# -*- coding: utf-8 -*-
from rest_framework import permissions
from core.permissions import PRIVILEGED, SUPER_USER, OPERATOR,AUDITOR


class DeliveryUpdateOrDelete(permissions.BasePermission):
    """
    Allows Only Manager or super user to update only to Super users.
    """
    ALLOWED_ROLES = [PRIVILEGED, SUPER_USER, OPERATOR,AUDITOR]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user
            and request.user.role
            and request.user.role in self.ALLOWED_ROLES
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER or request.user.role == PRIVILEGED:
            return True

        if (
            view.action in ["destroy", "update"]
            and request.user
            and request.user.is_authenticated
        ):
            ticket = obj.ticket
            if ticket.organization is not None:
                return request.user == obj.organization.manager
            elif not ticket.is_closed:
                return True
        return True
