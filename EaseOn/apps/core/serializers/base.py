# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from rest_framework import serializers

from .fields import DateTimeField


class BaseMeta:
    """
    Base Meta class for all models.
    make all audit field as read only
    """

    read_only_fields = ('is_deleted',)
    extra_kwargs = {
        'created_by': {'default': serializers.CurrentUserDefault()}
    }
    fields = '__all__'


class BaseSerializer(serializers.HyperlinkedModelSerializer):
    'Base Hyperlinked Model Serializer'
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_name',
        default=serializers.CurrentUserDefault(),
    )

    id = serializers.ReadOnlyField()
    created_at = serializers.DateTimeField(
        read_only=True, default=serializers.CreateOnlyDefault(timezone.now)
    )
    is_deleted = serializers.BooleanField(read_only=True)
    serializer_field_mapping = dict(
        serializers.HyperlinkedModelSerializer.serializer_field_mapping
    )
    serializer_field_mapping[models.DateTimeField] = DateTimeField

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(BaseSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['last_modified_by'] = self.context['request'].user
        if hasattr(instance, 'is_alive') and not instance.is_alive:
            raise serializers.ValidationError(
                'Can not update an object which has been deleted.'
            )
        return super(BaseSerializer, self).update(instance, validated_data)

    def get_user(self):
        return self.context['request'].user
