# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

from gsx import views
from core.router import DefaultRouter
from gsx.views import (
   GSXViewSet
)
from django.conf.urls import url
warranty = GSXViewSet.as_view({'post': 'warranty'})
diagnostic_suites = GSXViewSet.as_view({'post': 'diagnostic_suites'})
repair_eligibility = GSXViewSet.as_view({'post': 'repair_eligibility'})
diagnostics_lookup = GSXViewSet.as_view({'post': 'diagnostics_lookup'})
run_diagnosis_suite = GSXViewSet.as_view({'post': 'run_diagnosis_suite'})
diagnostics_status =  GSXViewSet.as_view({'post': 'diagnostics_status'})
urlpatterns = [
    url(r'warranty', warranty, name='warranty'),
    url(r'diagnostic_suites',diagnostic_suites,name='diagnostic_suites'),
    url(r'repair_eligibility',repair_eligibility,name='repair_eligibility'),
    url(r'diagnostics_lookup',diagnostics_lookup,name='diagnostics_lookup'),
    url(r'run_diagnosis_suite',run_diagnosis_suite,name='run_diagnosis_suite'),
    url(r'diagnostics_status',diagnostics_status,name='diagnostics_status'),

]
