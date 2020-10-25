# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from tickets import models, serializers


class CommentViewSet(viewsets.BaseViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    ordering = ["-id"]
