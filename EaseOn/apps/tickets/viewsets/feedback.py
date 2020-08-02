# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from tickets import models, serializers


class FeedbackViewSet(viewsets.BaseViewSet):
    queryset = models.Feedback.objects
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    serializer_class = serializers.FeedbackSerializer
