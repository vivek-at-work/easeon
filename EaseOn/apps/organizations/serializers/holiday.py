# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from organizations.models import Holiday
from rest_framework import serializers


class HolidaySerializer(BaseSerializer):
    """ """

    def validate(self, data):
        """
        Check that if record already exists..
        """
        count = Holiday.objects.filter(organization=data['organization'],date=data['data']).count()
        if count:
            raise serializers.ValidationError("Holiday Details Already Exists")
        return data

    class Meta(BaseMeta):
        model = Holiday
        fields = (
            'url',
            'created_by',
            'id',
            'created_at',
            'is_deleted',
            'date',
            'description',
            'organization',
        )
