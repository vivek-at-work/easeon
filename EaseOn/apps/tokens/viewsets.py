# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseViewSet
from django.db.models import Q
from tokens import models, serializers


class TokenFilter(django_filters.FilterSet):
    """Token Filter"""

    organization = django_filters.CharFilter(field_name='organization__code')

    class Meta:
        model = models.Token
        fields = ['token_number']


class TokenModelViewSet(BaseViewSet):
    serializer_class = serializers.TokenSerializer
    filter_class = TokenFilter
    search_fields = ('token_number', 'location_code', 'email')

    def get_queryset(self):
        return models.Token.objects.all()
