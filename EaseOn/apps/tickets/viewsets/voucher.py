# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from rest_framework import decorators, response,permissions,status
from tickets import models, serializers


class VoucherViewSet(viewsets.BaseViewSet):
    queryset = models.Voucher.objects.all()
    serializer_class = serializers.VoucherSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]

    @decorators.action(methods=["post"], detail=True)
    def cancel(self, request, pk=None):
        "add delivery details for the ticket."
        voucher = self.get_object()
        context = {"request": self.request}
        voucher.is_cancelled = True
        voucher.save()
        serializer = self.serializer_class(voucher, context=context)
        return response.Response(serializer.data)

    @decorators.action(methods=["post"], detail=True)
    def rollback(self, request, pk=None):
        "add delivery details for the ticket."
        voucher = self.get_object()
        context = {"request": self.request}
        voucher.is_cancelled = False
        voucher.save()
        serializer = self.serializer_class(voucher, context=context)
        return response.Response(serializer.data)

    @decorators.action(
        methods=["POST"],
        detail=True,
        url_path="upload_signature/(?P<reference_number>\w+)/(?P<guid>\w+)",
        serializer_class=serializers.VoucherSignatureSerializer,
        permission_classes = [permissions.AllowAny],
    )
    def upload_signature(self, request, pk,reference_number,guid):
        "Get diagnosis suites for device."
        voucher = self.get_object()
        if voucher.reference_number == reference_number and voucher.guid ==  guid:
            serializer = self.get_serializer_class()(
                voucher, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            headers = self.get_success_headers(serializer.data)
            obj = self.get_object()
            data = serializers.VoucherSerializer(obj, context={"request": request}).data
            return response.Response(data, status=status.HTTP_200_OK, headers=headers)
        return response.Response("Invalid paramters", status.HTTP_400_BAD_REQUEST)
