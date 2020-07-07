# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from .models import ReportRequest
from django.apps import apps
from lists.models import get_list_choices
from rest_framework import serializers
from customers.validators import validate_open_tickets

report_types = get_list_choices('REPORT_TYPES')

def get_organization_queryset():
    Organization = apps.get_model(*get_organization_model().split('.', 1))
    return Organization.objects.all()

class ReportRequestSerializer(BaseSerializer):
    report_type = serializers.ChoiceField(choices=report_types)
    organization= serializers.HyperlinkedRelatedField(
                queryset=get_organization_queryset(), view_name='organization-detail'
            )
    class Meta(BaseMeta):
        model = Customer
        fields = [
            'url',
            'organization',
            'start_date',
            'end_date',
            'report_type'
        ]
