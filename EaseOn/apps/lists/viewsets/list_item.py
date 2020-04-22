# -*- coding: utf-8 -*-
import django_filters
from core.permissions import SuperUserOrReadOnly
from core.utils.pagination import PageNumberPagination
from core.viewsets import BaseBulkCreateViewSet
from lists.models import LIST_NAME_CHOICES, Item
from lists.serializers import ItemModelSerializer
from rest_framework import decorators, response


class ListItemFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    list_name = django_filters.CharFilter()
    value = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = Item
        exclude = ()


# class ItemPagination(PageNumberPagination):
#     page_size = 1000
#     max_page_size = 1000


class ItemViewSet(BaseBulkCreateViewSet):
    serializer_class = ItemModelSerializer
    permission_classes = (SuperUserOrReadOnly,)
    # pagination_class = ItemPagination
    search_fields = ('list_name',)
    filter_class = ListItemFilter
    queryset = Item.objects.all()

    @decorators.action(methods=['GET'], detail=False)
    def list_types(self, request, pk=None):
        output = []
        for x, y in LIST_NAME_CHOICES:
            output.append({'key': x, 'display_text': y})
        return response.Response(output)
