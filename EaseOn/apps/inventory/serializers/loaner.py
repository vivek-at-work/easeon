# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from inventory.models import (
    LoanerInventoryItem,
    LoanerItemPenaltyAmount,
    RepairInventoryItem,
)
from lists.models import get_list_choices
from organizations.models import Organization
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class LoanerItemListSerializer(BaseSerializer):
    class Meta(BaseMeta):
        model = LoanerInventoryItem
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


class LoanerItemSerializer(BaseSerializer):
    def validate_uniques(self, key, value):
        d = {key: value}
        if not self.instance:
            if LoanerInventoryItem.objects.all().filter(**d).exists():
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing Loaner Inventory Item .'.format(
                        key
                    )
                )

        else:
            if (
                LoanerInventoryItem.objects.exclude(id=self.instance.id)
                .filter(**d)
                .exists()
            ):
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing Loaner Inventory Item.'.format(
                        key
                    )
                )
        if RepairInventoryItem.objects.all().filter(**d).exists():
            raise serializers.ValidationError(
                '{0} Already been used with previous existing Repair Inventory Item .'.format(
                    key
                )
            )

    def validate_serial_number(self, value):
        self.validate_uniques('serial_number', value)
        return value

    def validate_part_number(self, value):
        if not LoanerItemPenaltyAmount.objects.filter(
            part_number=value
        ).exists():
            raise serializers.ValidationError(
                'No Penalty Details exists for this part number {} .'.format(
                    value
                )
            )
        return value

    penalty = serializers.JSONField(read_only=True)

    serial_number = serializers.CharField(max_length=255,)
    part_number = serializers.ChoiceField(
        choices=get_list_choices('LOANER_INVENTORY_PART_NUMBERS')
    )

    def __init__(self, *args, **kwargs):
        super(LoanerItemSerializer, self).__init__(*args, **kwargs)
        # if 'view' in self.context:
        #     user = self.context['view'].request.user
        #     inventory_query = user.locations.filter(
        #         loaner_inventory=True
        #     )
        #     sp = inventory_query.values('organization')
        #     sps = Organization.objects.filter(id__in=sp)
        #     self.fields['organization'].queryset = sps

    class Meta(BaseMeta):
        model = LoanerInventoryItem
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


class PenaltyAmountSerializer(BaseSerializer):
    part_number = serializers.ChoiceField(
        choices=get_list_choices('LOANER_INVENTORY_PART_NUMBERS')
    )
    reason = serializers.ChoiceField(
        choices=get_list_choices('LOANER_INVENTORY_PENALTY_REASONS')
    )

    class Meta(BaseMeta):
        model = LoanerItemPenaltyAmount
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
            'last_modified_by',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=LoanerItemPenaltyAmount.objects.all(),
                message='Already Found Matching Penalty Entry.',
                fields=['part_number', 'reason'],
            )
        ]
