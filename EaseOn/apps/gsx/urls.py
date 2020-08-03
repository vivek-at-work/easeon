# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

from core.router import DefaultRouter
from django.conf.urls import url
from gsx import views
from gsx.views import GSXViewSet

warranty = GSXViewSet.as_view({'post': 'warranty'})
diagnostic_suites = GSXViewSet.as_view({'post': 'diagnostic_suites'})
repair_eligibility = GSXViewSet.as_view({'post': 'repair_eligibility'})
diagnostics_lookup = GSXViewSet.as_view({'post': 'diagnostics_lookup'})
run_diagnosis_suite = GSXViewSet.as_view({'post': 'run_diagnosis_suite'})
diagnostics_status = GSXViewSet.as_view({'post': 'diagnostics_status'})
consignment_validate = GSXViewSet.as_view({'post': 'consignment_validate'})
consignment_order_lookup = GSXViewSet.as_view(
    {'post': 'consignment_order_lookup'})
consignment_delivery_lookup = GSXViewSet.as_view(
    {'post': 'consignment_delivery_lookup'})
urlpatterns = [
    url(r'warranty', warranty, name='warranty'),
    url(r'diagnostic_suites', diagnostic_suites, name='diagnostic_suites'),
    url(r'repair_eligibility', repair_eligibility, name='repair_eligibility'),
    url(r'diagnostics_lookup', diagnostics_lookup, name='diagnostics_lookup'),
    url(
        r'run_diagnosis_suite', run_diagnosis_suite, name='run_diagnosis_suite'
    ),
    url(r'diagnostics_status', diagnostics_status, name='diagnostics_status'),
    url(r'consignment_validate', consignment_validate, name='consignment_validate'),
    url(r'consignment_order_lookup', consignment_order_lookup, name='consignment_order_lookup'),
    url(r'consignment_delivery_lookup', consignment_delivery_lookup, name='consignment_delivery_lookup'),
]
