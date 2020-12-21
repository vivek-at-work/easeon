# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

import logging

from core.permissions import IsOperatorOrSuperUser
from gsx import serializers
from gsx import serializers_uat
from rest_framework import permissions, response, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.urls import reverse
from django.urls import reverse_lazy
serializers_dict = {
    "warranty": serializers.DeviceSerializer,
    "diagnostic_suites": serializers.DiagnosticSuitesSerializer,
    "repair_eligibility": serializers.RepairEligibilitySerializer,
    "diagnostics_lookup": serializers.DiagnosticsLookupSerializer,
    "run_diagnosis_suite": serializers.RunDiagnosticsSerializer,
    "diagnostics_status": serializers.DiagnosticsStatusSerializer,
    "repair_summary": serializers.RepairSummarySerializer,
    "repair_details": serializers.RepairDetailsSerializer,
    "repair_audit": serializers.RepairAuditSerializer,
    "repair_questions": serializers.RepairQuestionsSerializer,
    "repair_create": serializers.RepairCreateSerializer,
    "part_summary": serializers.PartSummarySerializer,
    "repair_product_componentissue": serializers.ComponentIssueSerializer,
    "content_article_lookup": serializers.ContentArticleLookupSerializer,
    "content_article": serializers.ContentArticleSerializer,
    "consignment_order_lookup": serializers.ConsignmentOrderLookupSerializer,
    "consignment_delivery_lookup": serializers.ConsignmentDeliveryLookupSerializer,
    "technician_lookup": serializers.TechnicianLookupSerializer,
    "attachment_upload_access": serializers.AttachmentUploadAccessSerializer,
    "document_download": serializers.DocumentDownloadSerializer,
    "acknowledge_delivery": serializers.AcknowledgeDeliverySerializer,
    "invoice_summary":serializers_uat.InvoiceSummarySeralizer,
    "invoice_details":serializers_uat.InvoiceDetailsSerializer,
    "order_applecare_quote":serializers_uat.OrderAppleCareQuoteSerializer,
    "order_applecare_eligibility":serializers_uat.OrderAppleCareAgreementEligibilitySerializer,
    "order_applecare_create":serializers_uat.OrderAppleCareCreateSerializer,
    "order_applecare_summary":serializers_uat.OrderAppleCareSummarySerializer,
    "order_applecare_update":serializers_uat.OrderAppleCareUpdateSerializer,
    "order_applecare_delete":serializers_uat.OrderAppleCareDeleteSerializer,
    "order_stocking_parts_summary":serializers_uat.StockingOrderPartSummarySerializer,
    "order_stocking_create":serializers_uat.StockingOrderCreateSerializer,
    "order_stocking_summary":serializers_uat.StockingOrderSummarySerializer,
    "order_stocking_update":serializers_uat.StockingOrderUpdateSerializer,
    "escalation_create":serializers_uat.EscalationCreateSerializer,
    "escalation_details":serializers_uat.EscalationDetailsSerializer,
    "escalation_update":serializers_uat.EscalationUpdateSerializer,
    "attribute_lookup":serializers_uat.AttributeLookupSerializer
}
class GSXAPIMetaView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        l = serializers_dict.keys()
        data =[]
        for m in l :
            data.append({
                'method':m,
                'url':reverse('gsx:gsx_api_endpoint',
                kwargs={'action': m})
            })
        return response.Response(data,status=status.HTTP_200_OK)

class GSXAPIView(APIView):
    permission_classes = [AllowAny]
    def _validate(self, serializer, data):
        """
        :param serializer: serializer against which data to ve validated
        :param data: data to ve validated
        :return: serializer instance.
        """

        serializer_instance = serializer(data=data, context={"request": self.request})
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()

    def get_serializer_class(self,action):
        return serializers_dict.get(action, serializers.NoneSerializer)

    def post(self, request, action, format=None):
        serializer = self.get_serializer_class(action)
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)


