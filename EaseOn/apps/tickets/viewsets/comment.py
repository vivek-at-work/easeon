# -*- coding: utf-8 -*-
from core import viewsets
from tickets import models, serializers
from core.permissions import HasManagerRightsToUpdateOrDelete


class CommentViewSet(viewsets.BaseViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    ordering = ['-id']
