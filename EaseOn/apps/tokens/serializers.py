# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from core.utils import get_organization_model
from django.apps import apps
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tokens.models import Token


class TokenSerializer(BaseSerializer):
    organization_code = serializers.SlugRelatedField(
        read_only=True, slug_field='code', source='organization'
    )

    class Meta(BaseMeta):
        model = Token
        validators = [
            UniqueTogetherValidator(
                queryset=Token.objects.all().created_between(),
                fields=['token_number', 'location_code'],
            )
        ]
        extra_kwargs = {
            'created_by': {'default': serializers.CurrentUserDefault()}
        }
        fields = (
            'first_name',
            'organization_code',
            'last_name',
            'city',
            'country',
            'state',
            'address_line_1',
            'address_line_2',
            'street',
            'email',
            'contact_number',
            'pin_code',
            'location_code',
            'token_number',
        )

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        Organization = apps.get_model(*get_organization_model().split('.', 1))
        validated_data['organization'] = Organization.objects.get(
            token_machine_location_code=validated_data['location_code']
        )
        instance = Token.objects.create(**validated_data)
        return instance
