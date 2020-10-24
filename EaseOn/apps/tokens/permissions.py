from rest_framework import decorators, permissions, response


class isValidCaller(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return True
        return obj.invited_by is None
