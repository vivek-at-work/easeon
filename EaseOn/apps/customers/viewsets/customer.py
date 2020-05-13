# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseViewSet
from customers import models, serializers
from core.permissions import HasManagerRightsToUpdateOrDelete


class CustomerFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    contact_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = models.Customer
        fields = ['customer_type']


class CustomerViewSet(BaseViewSet):
    queryset = models.Customer.objects
    serializer_class = serializers.CustomerSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    search_fields = ('contact_number', 'email')
    filter_class = CustomerFilter
