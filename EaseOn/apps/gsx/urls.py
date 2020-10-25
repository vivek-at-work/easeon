# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

from core.router import DefaultRouter
from django.conf.urls import url
from gsx import views
from gsx.views import GSXViewSet

warranty = GSXViewSet.as_view({"post": "warranty"})
diagnostic_suites = GSXViewSet.as_view({"post": "diagnostic_suites"})
repair_eligibility = GSXViewSet.as_view({"post": "repair_eligibility"})
diagnostics_lookup = GSXViewSet.as_view({"post": "diagnostics_lookup"})
run_diagnosis_suite = GSXViewSet.as_view({"post": "run_diagnosis_suite"})
diagnostics_status = GSXViewSet.as_view({"post": "diagnostics_status"})
repair_summary = GSXViewSet.as_view({"post": "repair_summary"})
repair_details = GSXViewSet.as_view({"post": "repair_details"})
repair_audit = GSXViewSet.as_view({"post": "repair_audit"})
repair_product_componentissue = GSXViewSet.as_view(
    {"post": "repair_product_componentissue"}
)
part_summary = GSXViewSet.as_view({"post": "part_summary"})
content_article_lookup = GSXViewSet.as_view({"post": "content_article_lookup"})
content_article = GSXViewSet.as_view({"post": "content_article"})
consignment_order_lookup = GSXViewSet.as_view({"post": "consignment_order_lookup"})
consignment_delivery_lookup = GSXViewSet.as_view(
    {"post": "consignment_delivery_lookup"}
)
technician_lookup = GSXViewSet.as_view({"post": "technician_lookup"})
attachment_upload_access = GSXViewSet.as_view({"post": "attachment_upload_access"})
document_download = GSXViewSet.as_view({"post": "document_download"})
acknowledge_delivery = GSXViewSet.as_view({"post": "acknowledge_delivery"})
urlpatterns = [
    url(r"warranty", warranty, name="warranty"),
    url(r"diagnostic_suites", diagnostic_suites, name="diagnostic_suites"),
    url(r"repair_eligibility", repair_eligibility, name="repair_eligibility"),
    url(r"diagnostics_lookup", diagnostics_lookup, name="diagnostics_lookup"),
    url(r"run_diagnosis_suite", run_diagnosis_suite, name="run_diagnosis_suite"),
    url(r"diagnostics_status", diagnostics_status, name="diagnostics_status"),
    url(r"repair_summary", repair_summary, name="repair_summary"),
    url(r"repair_details", repair_details, name="repair_details"),
    url(r"repair_audit", repair_audit, name="repair_audit"),
    url(
        r"repair_product_componentissue",
        repair_product_componentissue,
        name="repair_product_componentissue",
    ),
    url(r"part_summary", part_summary, name="part_summary"),
    url(
        r"content_article_lookup", content_article_lookup, name="content_article_lookup"
    ),
    url(r"content_article", content_article, name="content_article"),
    url(
        r"consignment_order_lookup",
        consignment_order_lookup,
        name="consignment_order_lookup",
    ),
    url(
        r"consignment_delivery_lookup",
        consignment_delivery_lookup,
        name="consignment_delivery_lookup",
    ),
    url(r"technician_lookup", technician_lookup, name="technician_lookup"),
    url(
        r"attachment_upload_access",
        attachment_upload_access,
        name="attachment_upload_access",
    ),
    url(r"document_download", document_download, name="document_download"),
    url(r"acknowledge_delivery", acknowledge_delivery, name="acknowledge_delivery"),
]
