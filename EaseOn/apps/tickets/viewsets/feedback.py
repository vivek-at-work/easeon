# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers


class FeedbackViewSet(viewsets.BaseViewSet):
    queryset = models.Feedback.objects
    serializer_class = serializers.FeedbackSerializer
