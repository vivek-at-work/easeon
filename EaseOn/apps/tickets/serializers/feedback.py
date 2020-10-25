# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from rest_framework import serializers
from tickets import models


class FeedbackSerializer(BaseSerializer):
    ticket = serializers.HyperlinkedRelatedField(
        queryset=models.Ticket.objects.all(), view_name="ticket-detail"
    )

    class Meta(BaseMeta):
        model = models.Feedback
        read_only_fields = [
            "id",
            "url",
            "created_by",
            "created_at",
            "is_deleted",
            "guid",
            "updated_at",
            "deleted_at",
            "version",
            "last_visit_on",
            "last_modified_by",
        ]
