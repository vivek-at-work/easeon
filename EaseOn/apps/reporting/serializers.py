# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from core.utils import time_by_adding_business_days, get_organization_model
from .models import ReportRequest
from django.apps import apps
from lists.models import get_list_choices
from rest_framework import serializers
from customers.validators import validate_open_tickets
from django.conf import settings
import os
import uuid

report_types = get_list_choices('REPORT_TYPES')


def get_organization_queryset():
    Organization = apps.get_model(*get_organization_model().split('.', 1))
    return Organization.objects.all()


class ReportRequestSerializer(BaseSerializer):
    report_type = serializers.ChoiceField(choices=report_types)
    report_path = serializers.ReadOnlyField()
    is_processed = serializers.ReadOnlyField()
    organization_code = serializers.SlugRelatedField(
        source='organization', read_only=True, slug_field='code'
    )
    organization = serializers.HyperlinkedRelatedField(
        queryset=get_organization_queryset(), view_name='organization-detail'
    )

    class Meta(BaseMeta):
        model = ReportRequest
        fields = [
            'url',
            'organization',
            'organization_code',
            'start_date',
            'is_processed',
            'end_date',
            'report_type',
            'report_path',
        ]

    def _create_target_directory(self, relative_path):
        target_dir = os.path.join(settings.REPORTS_DIR, relative_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        return target_dir

    def _get_target_file_path(
        self, organization_code, report_type, file_name=None
    ):
        relative_path = "{}/{}".format(organization_code, report_type.lower())
        target_dir = self._create_target_directory(relative_path)
        if file_name:
            if not file_name.endswith('.csv'):
                file_name = "{}.csv".format(file_name)
        else:
            file_name = "{}.csv".format(str(uuid.uuid4()))
        return "{}/{}".format(relative_path, file_name)

    def create(self, validated_data):
        organization_code = validated_data['organization'].code
        report_type = validated_data['report_type']
        validated_data['report_path'] = self._get_target_file_path(
            organization_code, report_type
        )
        return super(ReportRequestSerializer, self).create(validated_data)
