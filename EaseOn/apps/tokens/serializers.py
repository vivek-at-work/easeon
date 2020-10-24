# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from core.utils import get_organization_model
from django.apps import apps
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tokens.models import Token
from django.contrib.auth import get_user_model


class TokenSerializer(BaseSerializer):
    organization_code = serializers.SlugRelatedField(
        read_only=True, slug_field='code', source='organization'
    )
    token_number = serializers.CharField(
        read_only=True,
    )
    counter_number = serializers.CharField(read_only=True)
    can_invite = serializers.SerializerMethodField()
    invited_by = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail'
    )
    technician_name = serializers.SlugRelatedField(
        read_only=True, slug_field='first_name', source='invited_by'
    )

    class Meta(BaseMeta):
        model = Token
        fields = (
            'url',
            'first_name',
            'location_code',
            'last_name',
            'token_number',
            'email',
            'organization_code',
            'contact_number',
            'counter_number',
            'invited_by',
            'technician_name',
            'invite_sent_on',
            'can_invite',
            'is_present',
        )

    def create(self, validated_data):
        validated_data['created_by'] = get_user_model().objects.first()
        Organization = apps.get_model(*get_organization_model().split('.', 1))
        validated_data['organization'] = Organization.objects.get(
            token_machine_location_code=validated_data['location_code']
        )
        validated_data['token_number'] = (
            Token.objects.filter(location_code=validated_data['location_code'])
            .created_between()
            .count()
            + 1
        )
        instance = Token.objects.create(**validated_data)
        instance.send_token_number_by_sms()
        return instance

    def get_can_invite(self, obj):
        requesting_user = self.context['request'].user
        return obj.can_invite(requesting_user)


class InviteCustomerSerilizer(serializers.Serializer):
    counter_number = serializers.IntegerField(min_value=1, max_value=50)
