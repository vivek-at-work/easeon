# -*- coding: utf-8 -*-
import django_filters
from core.models import SUPER_USER
from core.permissions import IsOperatorOrSuperUser
from core.viewsets import BaseViewSet
from customers import models, serializers


class HasRightsToUpdateOrDeleteCustomer(IsOperatorOrSuperUser):
    """
    Allows super user to update customers.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER:
            return True

        if (
            view.action in ["destroy", "update"]
            and request.user
            and request.user.is_authenticated
        ):
            return request.user.role == SUPER_USER

        return True


class CustomerFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    contact_number = django_filters.CharFilter(lookup_expr="icontains")

    class Meta(object):
        model = models.Customer
        fields = ["customer_type"]


class CustomerViewSet(BaseViewSet):
    queryset = models.Customer.objects
    serializer_class = serializers.CustomerSerializer
    permission_classes = [HasRightsToUpdateOrDeleteCustomer]
    search_fields = ("contact_number", "email")
    filter_class = CustomerFilter
