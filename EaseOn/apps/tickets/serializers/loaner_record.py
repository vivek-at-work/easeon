# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer, FileFieldWithLinkRepresentation
from inventory.models import LoanerInventoryItem
from inventory.serializers import LoanerItemSerializer
from rest_framework import serializers
from tickets.models import LoanerRecord, Ticket


class LoanerRecordSerializer(BaseSerializer):
    inventory_item = serializers.HyperlinkedRelatedField(
        queryset=LoanerInventoryItem.objects.all().available(),
        view_name="loanerinventoryitem-detail",
    )

    inventory_item_serial_number = serializers.ReadOnlyField(
        source="inventory_item.serial_number", read_only=True
    )
    inventory_item_description = serializers.ReadOnlyField(
        source="inventory_item.description", read_only=True
    )
    ticket = serializers.HyperlinkedRelatedField(
        queryset=Ticket.objects.all(), view_name="ticket-detail"
    )
    agreement = serializers.ReadOnlyField()
    customer_signature = FileFieldWithLinkRepresentation(read_only=True)

    class Meta(BaseMeta):

        model = LoanerRecord
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
            "is_lost",
            "returned_on",
            "penalty",
        ]
