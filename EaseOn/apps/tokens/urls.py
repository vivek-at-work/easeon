# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from tokens.viewsets import TokenModelViewSet

token_router = DefaultRouter()
token_router.register(r'tokens', TokenModelViewSet, basename='token')
