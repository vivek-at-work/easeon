# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    SerializableInventoryItemSerializer,
    SerializableInventoryListSerializer,
)
from core.permissions import IsOperatorOrSuperUser


class SerializableInventoryItemFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    description = django_filters.CharFilter(lookup_expr='icontains')
    created_at_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )
    created_at_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )

    class Meta(object):
        model = models.SerializableInventoryItem
        exclude = ()


class SerializableItemViewSet(BaseBulkCreateViewSet):
    filter_class = SerializableInventoryItemFilter
    serializer_class = SerializableInventoryItemSerializer
    list_serializer_class = SerializableInventoryListSerializer
    delete_serializer_class = SerializableInventoryListSerializer
    permission_classes = [IsOperatorOrSuperUser]
    ordering = ['id']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.SerializableInventoryItem.objects.all()
        else:
            organizations = self.request.user.locations.filter(
                non_serialized_inventory=True, is_active=True
            ).values_list('organization', flat=True)
            return models.SerializableInventoryItem.objects.filter(
                organization__in=organizations
            )
