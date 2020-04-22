# -*- coding: utf-8 -*-
from lists.viewsets import ItemViewSet
from rest_framework import routers

lists_router = routers.DefaultRouter()
lists_router.register(r'lists', ItemViewSet, basename='item')
