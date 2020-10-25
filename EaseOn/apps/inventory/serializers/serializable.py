# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from django.db.models import Q
from inventory.models import SerializableInventoryItem
from lists.models import get_list_choices
from organizations.models import Organization
from rest_framework import serializers

dc = get_list_choices("SERIALIZABLE_INVENTORY_ITEM")


class SerializableInventoryListSerializer(BaseSerializer):
    class Meta(BaseMeta):
        model = SerializableInventoryItem
        read_only_fields = [
            "id",
            "url",
            "created_by",
            "created_at",
            "is_deleted",
            "guid",
            "updated_at",
            "deleted_at",
            "version",
            "last_visit_on",
            "last_modified_by",
            "consumed",
            "blocked",
        ]


class SerializableInventoryItemSerializer(BaseSerializer):
    organization = serializers.HyperlinkedRelatedField(
        queryset=Organization.objects, view_name="organization-detail"
    )
    description = serializers.ChoiceField(choices=dc)

    def __init__(self, *args, **kwargs):
        super(SerializableInventoryItemSerializer, self).__init__(*args, **kwargs)
        # if 'view' in self.context:
        #     user = self.context['view'].request.user
        #     inventory_query = user.locations.filter(
        #         can_create_serializable_inventory=True
        #     )
        #     sp = inventory_query.values('organization')
        #     sps = Organization.objects.filter(id__in=sp)
        #     self.fields['organization'].queryset = sps

    class Meta(BaseMeta):

        model = SerializableInventoryItem
        read_only_fields = [
            "id",
            "url",
            "created_by",
            "created_at",
            "is_deleted",
            "guid",
            "updated_at",
            "deleted_at",
            "version",
            "last_visit_on",
            "last_modified_by",
            "available_quantity",
            "consumed_quantity",
        ]
