# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers
from core.permissions import HasManagerRightsToUpdateOrDelete


class FeedbackViewSet(viewsets.BaseViewSet):
    queryset = models.Feedback.objects
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    serializer_class = serializers.FeedbackSerializer
