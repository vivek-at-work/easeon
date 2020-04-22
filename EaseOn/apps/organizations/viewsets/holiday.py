# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseViewSet
from organizations.models import Holiday
from organizations.serializers import HolidaySerializer
from rest_framework import decorators, response


class HolidayFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    organization_code = django_filters.CharFilter(
        field_name='organization__code'
    )

    class Meta(object):
        model = Holiday
        fields = '__all__'


class HolidayViewSet(BaseViewSet):
    'A Service Provider  Membership View Set'
    serializer_class = HolidaySerializer
    filter_class = HolidayFilter

    def get_queryset(self):
        model = Holiday
        return model.objects.all()
