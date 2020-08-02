# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from core.utils import get_organization_model
from customers.validators import validate_open_tickets
from django.apps import apps
from lists.models import get_list_choices
from rest_framework import serializers

from .models import ReportRequest

report_types = get_list_choices('REPORT_TYPES')


def get_organization_queryset():
    Organization = apps.get_model(*get_organization_model().split('.', 1))
    return Organization.objects.all()


class ReportRequestSerializer(BaseSerializer):
    report_type = serializers.ChoiceField(choices=report_types)
    organization = serializers.HyperlinkedRelatedField(
        queryset=get_organization_queryset(), view_name='organization-detail'
    )

    class Meta(BaseMeta):
        model = ReportRequest
        fields = [
            'url',
            'organization',
            'start_date',
            'end_date',
            'report_type',
        ]
