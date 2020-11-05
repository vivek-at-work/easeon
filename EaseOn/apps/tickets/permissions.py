# -*- coding: utf-8 -*-
from core.permissions import AUDITOR, OPERATOR, PRIVILEGED, SUPER_USER
from rest_framework import permissions


class DeliveryUpdateOrDelete(permissions.BasePermission):
    """
    Allows Only Manager or super user to update only to Super users.
    """

    ALLOWED_ROLES = [PRIVILEGED, SUPER_USER, OPERATOR, AUDITOR]

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
            if not ticket.is_closed:
                return True
        return False
