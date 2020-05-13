# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    RepairItemListSerializer,
    RepairItemSerializer,
)

from core.permissions import IsOperatorOrSuperUser


class RepairInventoryItemFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

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
        model = models.RepairInventoryItem
        exclude = ()


class RepairItemViewSet(BaseBulkCreateViewSet):
    serializer_class = RepairItemSerializer
    list_serializer_class = RepairItemListSerializer
    delete_serializer_class = RepairItemListSerializer
    filter_class = RepairInventoryItemFilter
    permission_classes = [IsOperatorOrSuperUser]
    filter_fields = (
        'serial_number',
        'organization',
        'part_number',
        'description',
    )
    search_fields = ('serial_number', 'part_number', 'description')
    ordering = ['id']

    def get_queryset(self):
        return models.RepairInventoryItem.objects.all()
