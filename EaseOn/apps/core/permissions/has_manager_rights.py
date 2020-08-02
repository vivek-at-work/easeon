# -*- coding: utf-8 -*-
from .superuser import PRIVILEGED, SUPER_USER, IsOperatorOrSuperUser


class HasManagerRightsToUpdateOrDelete(IsOperatorOrSuperUser):
    """
    Allows Only Manager or super user to update only to Super users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER or request.user.role == PRIVILEGED:
            return True

        if (
            view.action in ['destroy', 'update']
            and request.user
            and request.user.is_authenticated
        ):
            if hasattr(obj, 'organization') and obj.organization is not None:
                return request.user == obj.organization.manager
            elif hasattr(obj, 'ticket') and obj.ticket is not None:
                return request.user == obj.ticket.organization.manager
        return True
