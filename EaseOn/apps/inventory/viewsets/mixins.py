# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response


class InventoryMixins(object):
    """docstring for InventoryMixins"""

    @action(detail=False)
    def defaults(self, request):
        data = {'can_create': True, 'consignment_type': 'Apple'}
        return Response(data)

    @action(detail=False)
    def part_lookup(self, request):
        data = {'description': 'Some description', 'is_serialized': True}
        return Response(data)
