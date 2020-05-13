# -*- coding: utf-8 -*-
from core import viewsets
from django.utils import timezone
from rest_framework import decorators, response
from tickets import models, serializers
from core.permissions import HasManagerRightsToUpdateOrDelete


class LoanerRecordViewSet(viewsets.BaseViewSet):
    queryset = models.LoanerRecord.objects.all()
    serializer_class = serializers.LoanerRecordSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]

    @decorators.action(methods=['post', 'GET'], detail=True)
    def mark_return(self, request, pk=None):
        'search applicable loaner items.'
        record = self.get_object()
        record.returned_on = timezone.now()
        record.is_lost = False
        record.save()
        serializer = self.serializer_class(
            record, context={'request': request}
        )
        return response.Response(serializer.data)

    @decorators.action(methods=['post', 'GET'], detail=True)
    def mark_lost(self, request, pk=None):
        'search applicable loaner items.'
        record = self.get_object()
        record.returned_on = None
        record.is_lost = True
        record.save()
        serializer = self.serializer_class(
            record, context={'request': request}
        )
        return response.Response(serializer.data)
