# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from lists.models import Item


class ItemModelSerializer(BaseSerializer):
    class Meta(BaseMeta):
        model = Item
