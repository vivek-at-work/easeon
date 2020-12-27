# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from django.db.models import Sum
from inventory.models import RepairInventoryItem, SerializableInventoryItem
from lists.models import get_list_choices
from rest_framework import serializers
from tickets.models import OrderLine, SerializableOrderLine, Ticket
from devices.models import ComponentIssue


class OrderLineSerializer(BaseSerializer):
    inventory_item = serializers.HyperlinkedRelatedField(
        queryset=RepairInventoryItem.objects.all().available(),
        view_name="repairinventoryitem-detail",
    )
    component_issue = serializers.HyperlinkedRelatedField(
        queryset=ComponentIssue.objects.all(),
        allow_null=True, required=False,
        view_name="componentissue-detail",
    )
    ticket = serializers.HyperlinkedRelatedField(
        queryset=Ticket.objects.all(), view_name="ticket-detail"
    )
    inventory_item_part_number = serializers.ReadOnlyField(
        source="inventory_item.part_number", read_only=True
    )
    inventory_item_serial_number = serializers.ReadOnlyField(
        source="inventory_item.serial_number", read_only=True
    )
    inventory_item_description = serializers.ReadOnlyField(
        source="inventory_item.description", read_only=True
    )

    class Meta(BaseMeta):
        model = OrderLine
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
        ]


class SerializableOrderLineSerializer(BaseSerializer):
    description = serializers.ChoiceField(
        choices=get_list_choices("SERIALIZABLE_INVENTORY_ITEM")
    )
    ticket = serializers.HyperlinkedRelatedField(
        queryset=Ticket.objects.all(), view_name="ticket-detail"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"] = serializers.ChoiceField(
            choices=get_list_choices("SERIALIZABLE_INVENTORY_ITEM")
        )

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if "view" in self.context:
            action = self.context["view"].action
            if action == "create":
                organization = data["ticket"].organization
                description = data["description"]
                quantity = data["quantity"]
                available_quantity = SerializableInventoryItem.objects.filter(
                    description=description, organization=organization
                ).aggregate(Sum("available_quantity"))
                val = available_quantity["available_quantity__sum"]
                if val is None:
                    val = 0
                if val < quantity:
                    msz = "quantity {0} for {2} not available,\
                        we have only {1} available"
                    raise serializers.ValidationError(
                        msz.format(quantity, val, description)
                    )
        return data

    class Meta(BaseMeta):
        model = SerializableOrderLine
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
        ]
