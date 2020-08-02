# -*- coding: utf-8 -*-
import django_filters
from core.permissions import IsOperatorOrSuperUser
from core.viewsets import BaseBulkCreateViewSet
from django.db.models import Q
from inventory import models
from inventory.serializers import (LoanerItemListSerializer,
                                   LoanerItemSerializer,
                                   PenaltyAmountSerializer)


class LoanerInventoryItemFilter(django_filters.FilterSet):
    """Filter Set Class for Loaner Inventory"""

    po_number = django_filters.CharFilter(lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    part_number = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    created_at_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )
    created_at_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )

    class Meta(object):
        model = models.LoanerInventoryItem
        exclude = ()


class LoanerItemViewSet(BaseBulkCreateViewSet):
    """View Set for loaner inventory"""

    rights_for = 'loaner_inventory'
    serializer_class = LoanerItemSerializer
    list_serializer_class = LoanerItemListSerializer
    delete_serializer_class = LoanerItemListSerializer
    filter_class = LoanerInventoryItemFilter
    permission_classes = [IsOperatorOrSuperUser]
    ordering = ['id']
    filter_fields = (
        'serial_number',
        'organization',
        'part_number',
        'description',
    )
    search_fields = ('serial_number', 'part_number', 'description')

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_privileged:
            return models.LoanerInventoryItem.objects.all()
        else:
            (
                organizations,
                managed_organizations,
            ) = self.get_user_organizations()
            return models.LoanerInventoryItem.objects.filter(
                Q(organization__in=organizations)
                | Q(organization__in=managed_organizations)
            )


class PenaltyAmountViewSet(BaseBulkCreateViewSet):
    """View Set for loaner inventory Item Penalty Create/Update"""

    serializer_class = PenaltyAmountSerializer
    search_fields = ('part_number',)

    def get_queryset(self):
        return models.LoanerItemPenaltyAmount.objects.all()
