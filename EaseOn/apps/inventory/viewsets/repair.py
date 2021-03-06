# -*- coding: utf-8 -*-
import django_filters
from core.permissions import IsOperatorOrSuperUser
from core.viewsets import BaseBulkCreateViewSet
from django.db.models import Q
from inventory import models
from inventory.serializers import RepairItemListSerializer, RepairItemSerializer


class RepairInventoryItemFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    po_number = django_filters.CharFilter(lookup_expr="icontains")
    serial_number = django_filters.CharFilter(lookup_expr="icontains")
    part_number = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    organization = django_filters.CharFilter(field_name="organization__code")
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )

    class Meta(object):
        model = models.RepairInventoryItem
        exclude = ()


class RepairItemViewSet(BaseBulkCreateViewSet):
    rights_for = "repair_inventory"
    serializer_class = RepairItemSerializer
    list_serializer_class = RepairItemListSerializer
    delete_serializer_class = RepairItemListSerializer
    filter_class = RepairInventoryItemFilter
    permission_classes = [IsOperatorOrSuperUser]
    filter_fields = ("serial_number", "organization", "part_number", "description")
    search_fields = ("serial_number", "part_number", "description")

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_privileged:
            return models.RepairInventoryItem.objects.all()
        else:
            (organizations, managed_organizations) = self.get_user_organizations()
            return models.RepairInventoryItem.objects.filter(
                Q(organization__in=organizations)
                | Q(organization__in=managed_organizations)
            )
