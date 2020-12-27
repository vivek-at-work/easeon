# -*- coding: utf-8 -*-
import django_filters
from core import permissions, viewsets
from rest_framework import decorators, response
from slas import models, serializers


class SLAFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    sla_type = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta(object):
        model = models.SLA
        exclude = ()


class SLAViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.SLASerializer
    queryset = models.SLA.objects.all()
    permission_classes = [permissions.SuperUserOrReadOnly]
    filter_class = SLAFilter


class TermViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.TermSerializer
    queryset = models.Term.objects.all()
    permission_classes = [permissions.SuperUserOrReadOnly]
