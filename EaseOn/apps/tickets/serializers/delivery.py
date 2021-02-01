# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer, FileFieldWithLinkRepresentation
from rest_framework import serializers
from tickets import models


class DeliverySerializer(BaseSerializer):
    """Delivery Model Serializer """

    ticket = serializers.HyperlinkedRelatedField(
        queryset=models.Ticket.objects.all(), view_name="ticket-detail"
    )
    reference_number = serializers.CharField(
        source="ticket.reference_number", read_only=True
    )
    unit_part_reports = serializers.JSONField(
        required=False, initial=dict, allow_null=True
    )
    customer_signature = FileFieldWithLinkRepresentation(read_only=True)
    delivery_done_by_name = serializers.SlugRelatedField(
        source="delivery_done_by", read_only=True, slug_field="full_name"
    )

    class Meta(BaseMeta):
        model = models.Delivery
        read_only_fields = [
            "url",
            "id",
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
