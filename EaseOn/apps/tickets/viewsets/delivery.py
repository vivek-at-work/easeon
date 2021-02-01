# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
from core import viewsets
from rest_framework import decorators, permissions, response, status
from tickets import models, serializers
from tickets.permissions import DeliveryUpdateOrDelete


class DeliveryViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.DeliverySerializer
    permission_classes = [DeliveryUpdateOrDelete]

    def get_queryset(self):
        return models.Delivery.objects.all()

    @decorators.action(
        methods=["POST"],
        detail=True,
        serializer_class=serializers.DeliverySignatureSerializer,
        url_path="upload_signature/(?P<reference_number>\w+)/(?P<guid>\w+)",
        permission_classes=[permissions.AllowAny],
    )
    def upload_signature(self, request, pk, reference_number, guid):
        "Get diagnosis suites for device."
        delivery = self.get_object()
        ticket = delivery.ticket
        if ticket.reference_number == reference_number and delivery.guid == guid:
            serializer = self.get_serializer_class()(
                delivery, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            headers = self.get_success_headers(serializer.data)
            obj = self.get_object()
            data = self.serializer_class(obj, context={"request": request}).data
            return response.Response(data, status=status.HTTP_200_OK, headers=headers)
        return response.Response("Invalid paramters", status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        methods=["POST"],
        detail=True,
        serializer_class=serializers.SaveCustomerFeedbackSerializer,
        url_path="save_feedback/(?P<reference_number>\w+)/(?P<guid>\w+)",
        permission_classes=[permissions.AllowAny],
    )
    def save_feedback(self, request, pk, reference_number, guid):
        "Get diagnosis suites for device."
        delivery = self.get_object()
        ticket = delivery.ticket
        if ticket.reference_number == reference_number and delivery.guid == guid:
            serializer = self.get_serializer_class()(
                delivery, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                delivery.customer_feedback = serializer.validated_data[
                    "customer_feedback"
                ]
                delivery.save()
            headers = self.get_success_headers(serializer.data)
            obj = self.get_object()
            data = self.serializer_class(obj, context={"request": request}).data
            return response.Response(data, status=status.HTTP_200_OK, headers=headers)
        return response.Response("Invalid paramters", status.HTTP_400_BAD_REQUEST)

    
    @decorators.action(methods=["post", "get"], detail=True, url_name="delivery_pdf")
    def pdf(self, request, pk):
        """Generate pdf."""
        delivery = self.get_object()
        output, name = delivery.get_pdf()
        response = HttpResponse(content_type="application/pdf;")
        response["Content-Disposition"] = "inline; filename=delivery.pdf"
        response["Content-Transfer-Encoding"] = "binary"
        response.write(output)
        return response
