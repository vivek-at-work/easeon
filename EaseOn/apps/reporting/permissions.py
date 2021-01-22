
# -*- coding: utf-8 -*-
from core.permissions.superuser import PRIVILEGED, SUPER_USER, IsOperatorOrSuperUser


class HasReportDownloadPermissions(IsOperatorOrSuperUser):
    """
    Allows Only Manager or super user to update only to Super users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER or request.user.role == PRIVILEGED:
            return True

        if (
            view.action in ["download"]
            and request.user
            and request.user.is_authenticated
        ):
            if hasattr(obj, "organization") and obj.organization is not None:
                return request.user == obj.organization.manager
        return True