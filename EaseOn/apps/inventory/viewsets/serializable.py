# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseBulkCreateViewSet
from inventory import models
from inventory.serializers import (
    SerializableInventoryItemSerializer,
    SerializableInventoryListSerializer,
)
from core.permissions import IsOperatorOrSuperUser
from django.db.models import Q

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
    rights_for = 'non_serialized_inventory'
    filter_class = SerializableInventoryItemFilter
    serializer_class = SerializableInventoryItemSerializer
    list_serializer_class = SerializableInventoryListSerializer
    delete_serializer_class = SerializableInventoryListSerializer
    permission_classes = [IsOperatorOrSuperUser]
    ordering = ['id']

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_privileged:
            return models.SerializableInventoryItem.objects.all()
        else:
            organizations , managed_organizations = self.get_user_organizations()
            return models.SerializableInventoryItem.objects.filter(
               Q(organization__in=organizations) | Q(organization__in=managed_organizations))