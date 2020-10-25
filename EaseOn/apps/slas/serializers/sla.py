# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from rest_framework import serializers
from slas.models import SLA, Term


class TermSerializer(BaseSerializer):
    class Meta(BaseMeta):
        model = Term
        fields = ("url", "statement", "sla", "heading")


class SLASerializer(BaseSerializer):
    terms = TermSerializer(many=True, read_only=True)

    class Meta(BaseMeta):
        model = SLA
        fields = ("url", "sla_type", "name", "is_default", "terms")
