# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from organizations.models import Holiday
from rest_framework import serializers


class HolidaySerializer(BaseSerializer):
    """ """

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
