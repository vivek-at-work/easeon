# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    RepairItemListSerializer,
    RepairItemSerializer,
)


class RepairInventoryItemFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    po_number = django_filters.CharFilter(lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    part_number = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = models.RepairInventoryItem
        exclude = ()


class RepairItemViewSet(BaseBulkCreateViewSet):
    serializer_class = RepairItemSerializer
    list_serializer_class = RepairItemListSerializer
    delete_serializer_class = RepairItemListSerializer
    filter_class = RepairInventoryItemFilter
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
