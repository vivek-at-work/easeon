# -*- coding: utf-8 -*-
from core import utils
from django.contrib.auth import get_user_model
from lists.models import Item
from lists.serializers import ItemModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse
from slas.models import SLA
from slas.serializers import SLASerializer

USER_MODEL = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_active = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()
    can_update = serializers.SerializerMethodField()

    class Meta:
        model = USER_MODEL
        fields = (
            'id',
            'url',
            'email',
            'first_name',
            'city',
            'pin_code',
            'last_name',
            'full_name',
            'date_joined',
            'contact_number',
            'is_active',
            'is_superuser',
            'gsx_technician_id',
            'gsx_ship_to',
            'gsx_user_name',
            'can_update',
            'role',
        )

    def get_can_update(self, obj):
        requesting_user = self.context['request'].user
        return requesting_user.is_superuser and (requesting_user.id != obj.id)


class ChangeUserRoleSerializer(serializers.Serializer):
    user_type = serializers.ChoiceField(choices=USER_MODEL.USER_TYPE_CHOICES)
