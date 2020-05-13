# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from lists.models import Item, LIST_NAME_CHOICES
from rest_framework import serializers


class ItemModelSerializer(BaseSerializer):
    def validate_list_name(self, value):
        """
        Check that list_name is valid.
        """
        user = self.get_user()
        if user.is_superuser:
            valid_list_names = [x for x, y in LIST_NAME_CHOICES]
            if value not in valid_list_names:
                raise serializers.ValidationError('Not a valid list type.')
        elif value not in ['SERIALIZABLE_INVENTORY_ITEM']:
            raise serializers.ValidationError('You can not create this Item.')

        return value

    class Meta(BaseMeta):
        model = Item
