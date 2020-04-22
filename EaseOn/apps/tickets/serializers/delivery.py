# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from rest_framework import serializers
from tickets import models


class DeliverySerializer(BaseSerializer):
    """Delivery Model Serializer """

    ticket = serializers.HyperlinkedRelatedField(
        queryset=models.Ticket.objects.all(), view_name='ticket-detail'
    )
    reference_number = serializers.CharField(read_only=True)

    def validate(self, values):
        if (
            values['ticket']
            .organization.holidays.filter(
                date=values['device_pickup_time'].date()
            )
            .exists()
        ):
            raise serializers.ValidationError(
                'Not a valid device pickup time.'
            )
        return values

    class Meta(BaseMeta):
        model = models.Delivery
        read_only_fields = [
            'url',
            'created_by',
            'created_at',
            'is_deleted',
            'guid',
            'updated_at',
            'deleted_at',
            'version',
            'last_visit_on',
            'last_modified_by',
        ]
