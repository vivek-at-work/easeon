# -*- coding: utf-8 -*-
from core.router import DefaultRouter
from django.conf.urls import url
from tickets.viewsets import (
    CommentViewSet,
    DeliveryViewSet,
    DevicePartReportViewSet,
    GSXInfoViewSet,
    LoanerRecordViewSet,
    OrderLineViewSet,
    SerializableOrderLineViewSet,
    TicketViewSet,
    VoucherViewSet,
)

ticket_router = DefaultRouter()
ticket_router.register(r"tickets", TicketViewSet, basename="ticket")
ticket_router.register(r"comments", CommentViewSet, basename="comment")
ticket_router.register(r"vouchers", VoucherViewSet, basename="voucher")
ticket_router.register(r"loanerrecords", LoanerRecordViewSet, basename="loanerrecord")
ticket_router.register(r"orderlines", OrderLineViewSet, basename="orderline")
ticket_router.register(
    r"serializable_orderlines",
    SerializableOrderLineViewSet,
    basename="serializableorderline",
)
ticket_router.register(r"deliveries", DeliveryViewSet, basename="delivery")
ticket_router.register(
    r"device_part_reports", DevicePartReportViewSet, basename="devicepartreport"
)
ticket_router.register(r"gsx_info", GSXInfoViewSet, basename="gsxinfo")
