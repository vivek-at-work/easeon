# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from django.db import transaction
from rest_framework import decorators, response, status
from tickets import models, serializers


class OrderLineViewSet(viewsets.BaseBulkCreateViewSet):
    """
    A simple ViewSet for viewing comments.
    """

    queryset = models.OrderLine.objects.all()
    serializer_class = serializers.OrderLineSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]

    def destroy(self, request, *args, **kwargs):
        try:
            record = self.get_object()
            with transaction.atomic():
                record.delete()
                record.inventory_item.consumed = False
                record.inventory_item.save()
                serializer = self.serializer_class(
                    record, context={'request': request}
                )
                return response.Response(serializer.data)
        except Exception:
            pass
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SerializableOrderLineViewSet(viewsets.BaseViewSet):
    queryset = models.SerializableOrderLine.objects.all()
    serializer_class = serializers.SerializableOrderLineSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            record = self.get_object()
            with transaction.atomic():
                record.delete()
                serializer = self.serializer_class(
                    record, context={'request': request}
                )
                return response.Response(serializer.data)
        except Exception:
            pass
        return response.Response(status=status.HTTP_204_NO_CONTENT)
