from .superuser import SUPER_USER,IsOperatorOrSuperUser

class HasManagerRightsToUpdateOrDelete(IsOperatorOrSuperUser):
    """
    Allows Only Manager or super user to update only to Super users.
    """

    ALLOWED_ROLES = [SUPER_USER]

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER:
            return True

        if (
            view.action
            in [
                'destroy','update'
            ]
            and request.user
            and request.user.is_authenticated
        ):  
            if hasattr(obj, 'organization') and obj.organization is not None:
                return (
                    request.user == obj.organization.manager
                )
            elif hasattr(obj, 'ticket') and obj.ticket is not None:
                return (
                    request.user == obj.ticket.organization.manager
                )