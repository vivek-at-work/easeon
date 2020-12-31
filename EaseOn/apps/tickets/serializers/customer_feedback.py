# -*- coding: utf-8 -*-
from core.serializers import (
    BaseMeta,
    BaseSerializer,
    FileFieldWithLinkRepresentation,
    UserSerializer,
)
from rest_framework import serializers
from tickets import models


class SaveCustomerFeedbackSerializer(BaseSerializer):
    """
    Used in Post/and put  requests
    """

    customer_feedback = serializers.JSONField(initial=dict)

    class Meta(BaseMeta):
        model = models.Delivery
