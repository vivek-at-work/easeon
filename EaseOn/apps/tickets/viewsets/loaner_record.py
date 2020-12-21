# -*- coding: utf-8 -*-
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from django.utils import timezone
from rest_framework import decorators, permissions, response, status
from tickets import models, serializers


class LoanerRecordViewSet(viewsets.BaseViewSet):
    queryset = models.LoanerRecord.objects.all()
    serializer_class = serializers.LoanerRecordSerializer
    permission_classes = [HasManagerRightsToUpdateOrDelete]

    @decorators.action(methods=["post", "GET"], detail=True)
    def mark_return(self, request, pk=None):
        "search applicable loaner items."
        record = self.get_object()
        record.returned_on = timezone.now()
        record.is_lost = False
        record.save()
        serializer = self.serializer_class(record, context={"request": request})
        return response.Response(serializer.data)

    @decorators.action(methods=["post", "GET"], detail=True)
    def mark_lost(self, request, pk=None):
        "search applicable loaner items."
        record = self.get_object()
        record.returned_on = None
        record.is_lost = True
        record.save()
        serializer = self.serializer_class(record, context={"request": request})
        return response.Response(serializer.data)

    @decorators.action(
        methods=["POST"],
        detail=True,
        url_path="upload_signature/(?P<reference_number>\w+)/(?P<guid>\w+)",
        serializer_class=serializers.LoanerRecordSignatureSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def upload_signature(self, request, pk, reference_number, guid):
        "Get diagnosis suites for device."
        loanerRecord = self.get_object()
        if (
            loanerRecord.ticket.reference_number == reference_number
            and loanerRecord.guid == guid
        ):
            serializer = self.get_serializer_class()(
                loanerRecord,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            headers = self.get_success_headers(serializer.data)
            obj = self.get_object()
            data = self.serializer_class(obj, context={"request": request}).data
            return response.Response(data, status=status.HTTP_200_OK, headers=headers)
        return response.Response("Invalid paramters", status.HTTP_400_BAD_REQUEST)
