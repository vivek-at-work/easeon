# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from rest_framework import serializers
from tickets import models


class CommentSerializer(BaseSerializer):
    ticket = serializers.HyperlinkedRelatedField(
        queryset=models.Ticket.objects.all(), view_name="ticket-detail"
    )

    class Meta(BaseMeta):
        model = models.Comment
        read_only_fields = ["url", "created_by", "created_at", "is_deleted"]
