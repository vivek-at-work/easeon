# -*- coding: utf-8 -*-
from rest_framework import serializers

RESOURCE_CHOICES = [
    "technician/lookup",
    "parts/summary",
    "attachment/upload-access",
    "document-download",
    "content/article/lookup",
    "consignment/order/submit",
    "consignment/delivery/lookup",
    "consignment/order/lookup",
    "consignment/order/shipment",
    "consignment/delivery/acknowledge",
    "consignment/validate",
    "diagnostics/status",
    "diagnostics/customer-report-url",
    "diagnostics/lookup",
    "diagnostics/suites",
    "repair/product/serializer/lookup",
    "repair/product/details",
    "repair/product/componentissue",
    "repair/create",
    "repair/loaner/return",
    "repair/questions",
    "repair/product/serializer",
    "repair/audit",
    "repair/update",
    "repair/eligibility",
    "repair/details",
    "repair/summary",
    "authenticate/end-session",
    "authenticate/token",
    "authenticate/check",
]


class GSXPayloadSerializer(serializers.Serializer):
    payload = serializers.JSONField(binary=True)
    method = serializers.ChoiceField(choices=["GET", "POST"])
    resource_name = serializers.ChoiceField(choices=RESOURCE_CHOICES)
