# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from inventory.models import LoanerInventoryItem, RepairInventoryItem
from organizations.models import Organization
from rest_framework import serializers


class RepairItemListSerializer(BaseSerializer):



    class Meta(BaseMeta):
        model = RepairInventoryItem
        read_only_fields = [
            'id',
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
            'consumed',
            'blocked',
        ]


class RepairItemSerializer(BaseSerializer):
    def validate_uniques(self, key, value):
        d = {key: value}
        if not self.instance:
            if RepairInventoryItem.objects.all().filter(**d).exists():
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing Repair Inventory Item .'.format(
                        key
                    )
                )

        else:
            if (
                RepairInventoryItem.objects.exclude(id=self.instance.id)
                .filter(**d)
                .exists()
            ):
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing Repair Inventory Item.'.format(
                        key
                    )
                )
        if LoanerInventoryItem.objects.all().filter(**d).exists():
            raise serializers.ValidationError(
                '{0} Already been used with previous existing Loaner Inventory Item .'.format(
                    key
                )
            )

    def validate_serial_number(self, value):
        self.validate_uniques('serial_number', value)
        return value

    organization = serializers.HyperlinkedRelatedField(
        queryset=Organization.objects.all(), view_name='organization-detail'
    )
    serial_number = serializers.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(RepairItemSerializer, self).__init__(*args, **kwargs)
        # if 'view' in self.context:
        #     user = self.context['view'].request.user
        #     inventory_query = user.locations.filter(
        #         reapir_inventory=True
        #     )
        #     sp = inventory_query.values('organization')
        #     sps = Organization.objects.filter(id__in=sp)
        #     self.fields['organization'].queryset = sps

    class Meta(BaseMeta):
        model = RepairInventoryItem
        read_only_fields = [
            'id',
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
            'consumed',
            'blocked',
        ]
