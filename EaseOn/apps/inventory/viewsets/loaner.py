# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    LoanerItemListSerializer,
    LoanerItemSerializer,
    PenaltyAmountSerializer,
)


class LoanerInventoryItemFilter(django_filters.FilterSet):
    """Filter Set Class for Loaner Inventory"""

    po_number = django_filters.CharFilter(lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    part_number = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = models.LoanerInventoryItem
        exclude = ()


class LoanerItemViewSet(BaseBulkCreateViewSet):
    """View Set for loaner inventory"""

    serializer_class = LoanerItemSerializer
    list_serializer_class = LoanerItemListSerializer
    delete_serializer_class = LoanerItemListSerializer
    filter_class = LoanerInventoryItemFilter
    ordering = ['id']
    filter_fields = (
        'serial_number',
        'organization',
        'part_number',
        'description',
    )
    search_fields = ('serial_number', 'part_number', 'description')

    def get_queryset(self):
        return models.LoanerInventoryItem.objects


class PenaltyAmountViewSet(BaseBulkCreateViewSet):
    """View Set for loaner inventory Item Penalty Create/Update"""

    serializer_class = PenaltyAmountSerializer
    search_fields = ('part_number',)

    def get_queryset(self):
        return models.LoanerItemPenaltyAmount.objects.all()
