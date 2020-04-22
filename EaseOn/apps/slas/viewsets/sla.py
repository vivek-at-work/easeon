# -*- coding: utf-8 -*-
import django_filters
from core import permissions, viewsets
from rest_framework import decorators, response
from slas import models, serializers


class SLAFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    sla_type = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = models.SLA
        exclude = ()


class SLAViewSet(viewsets.BaseReadOnlyViewSet):
    serializer_class = serializers.SLASerializer
    queryset = models.SLA.objects.all()
    permission_classes = [permissions.SuperUserOrReadOnly]
    filter_class = SLAFilter
    # @decorators.action(detail=False, methods=['get'])
    # def get_ticket_slas(self, request, pk=None):
    #     slas = self.get_queryset().filter(sla_type='TICKET_SLA')
    #     serializer = self.serializer_class(
    #         slas, context={'request': request}, many=True
    #     )
    #     return response.Response({'results': serializer.data})

    # @decorators.action(detail=False, methods=['get'])
    # def get_delivery_slas(self, request, pk=None):
    #     slas = self.get_queryset().filter(sla_type='DELIVERY_SLA')
    #     serializer = self.serializer_class(
    #         slas, context={'request': request}, many=True
    #     )
    #     return response.Response({'results': serializer.data})

    # @decorators.action(detail=False, methods=['get'])
    # def get_phone_loan_agreement_slas(self, request, pk=None):
    #     slas = self.get_queryset().filter(sla_type='PHONE_LOAN_AGREEMENT')
    #     serializer = self.serializer_class(
    #         slas, context={'request': request}, many=True
    #     )
    #     return response.Response({'results': serializer.data})


class TermViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.TermSerializer
    queryset = models.Term.objects.all()
    permission_classes = [permissions.SuperUserOrReadOnly]
