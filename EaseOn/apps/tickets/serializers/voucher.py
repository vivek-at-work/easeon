# -*- coding: utf-8 -*-
"""
Voucher Serializer
"""
from core.serializers import BaseMeta, BaseSerializer,FileFieldWithLinkRepresentation
from django.db import transaction
from rest_framework import serializers
from tickets import models


class VoucherSerializer(BaseSerializer):
    """
    Voucher Serializer
    """

    ticket = serializers.HyperlinkedRelatedField(
        queryset=models.Ticket.objects.all(), view_name="ticket-detail"
    )

    total_amount = serializers.ReadOnlyField()
    actual_payment_modes = serializers.ReadOnlyField()
    customer_signature = FileFieldWithLinkRepresentation(read_only=True)

    class Meta(BaseMeta):
        model = models.Voucher
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
            "reference_number",
            "is_cancelled",
            "total_amount",
            "organization",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            ticket = validated_data.get("ticket")
            reference_number = "{0}{1}{2}".format(
                ticket.reference_number,
                ticket.vouchers.count(),
                models.Voucher.all_objects.count(),
            )
            validated_data["reference_number"] = reference_number
            instance = super(VoucherSerializer, self).create(validated_data)
            return instance
