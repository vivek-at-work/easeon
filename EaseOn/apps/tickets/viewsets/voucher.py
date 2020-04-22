# -*- coding: utf-8 -*-
from core import viewsets
from rest_framework import decorators, response
from tickets import models, serializers


class VoucherViewSet(viewsets.BaseViewSet):
    queryset = models.Voucher.objects.all()
    serializer_class = serializers.VoucherSerializer

    @decorators.action(methods=['post'], detail=True)
    def cancel(self, request, pk=None):
        'add delivery details for the ticket.'
        voucher = self.get_object()
        context = {'request': self.request}
        voucher.is_cancelled = True
        voucher.save()
        serializer = self.serializer_class(voucher, context=context)
        return response.Response(serializer.data)
    
    @decorators.action(methods=['post'], detail=True)
    def rollback(self, request, pk=None):
        'add delivery details for the ticket.'
        voucher = self.get_object()
        context = {'request': self.request}
        voucher.is_cancelled = False
        voucher.save()
        serializer = self.serializer_class(voucher, context=context)
        return response.Response(serializer.data)
