# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from customers.viewsets import CustomerViewSet

customer_router = DefaultRouter()
customer_router.register(r'customers', CustomerViewSet, basename='customer')
