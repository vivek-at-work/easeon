# -*- coding: utf-8 -*-
from core import utils
from core.serializers import BaseMeta, BaseSerializer
from devices.models import ComponentIssue, Device
from devices.validators import (
    validate_identifier,
    validate_open_tickets,
    validate_restricted_device,
)
from rest_framework import serializers


class ComponentIssueSerializer(BaseSerializer):
    """A Component Issue"""

    device = serializers.HyperlinkedRelatedField(
        queryset=Device.objects, view_name="device-detail"
    )

    class Meta(BaseMeta):
        model = ComponentIssue
        fields = [
            "url",
            "component_code",
            "component_description",
            "issue_code",
            "issue_description",
            "priority",
            "order",
            "device",
            "reproducibility",
            "is_technician_verified",
        ]
