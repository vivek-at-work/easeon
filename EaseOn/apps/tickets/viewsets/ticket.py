# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
import os
import tempfile

import django_filters
from core import viewsets
from core.models import AUDITOR, PRIVILEGED, SUPER_USER
from core.permissions import HasManagerRightsToUpdateOrDelete
from devices.validators import gsx_validate
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from gsx.converters import get_convertor_class
from gsx.serializers import (
    ComponentIssueSerializer,
    RepairEligibilitySerializer,
    RepairQuestionsSerializer,
)
from inventory.serializers import LoanerItemSerializer, RepairItemSerializer
from rest_framework import decorators, permissions, response, status
from rest_framework.parsers import MultiPartParser
from tickets import models, serializers
from tickets.permissions import TicketPermissions
from weasyprint import CSS, HTML


class UserNameFilter(django_filters.CharFilter):
    empty_value = "EMPTY"

    def filter(self, qs, value):
        if value:
            first_name = value.split()[0]
            f_name = self.field_name + "__first_name"
            d = {f_name: first_name}
            qs = qs.filter(**d)
            if len(value.split()) > 1:
                last_name = value.split()[1]
                l_name = self.field_name + "__last_name"
                d = {l_name: last_name}
                qs = qs.filter(**d)
        return qs


class DeviceFilter(django_filters.CharFilter):
    empty_value = "EMPTY"

    def filter(self, qs, value):
        if value:
            if gsx_validate(value, "alternateDeviceId"):
                d = {"device__alternateDeviceId": value}
            elif gsx_validate(value, "serialNumber"):
                d = {"device__serial_number": value}
            elif gsx_validate(value, "productName"):
                d = {"device__product_name": value}
            else:
                return qs
            qs = qs.filter(**d)
        return qs


class CustomerFilter(django_filters.CharFilter):
    empty_value = "EMPTY"

    def filter(self, qs, value):
        if value:
            cn_d = {f"{self.field_name}__contact_number": value}
            al_cn_d = {f"{self.field_name}__alternate_contact_number": value}
            em_d = {f"{self.field_name}__email": value}
            return qs.filter(Q(**cn_d) | Q(**al_cn_d) | Q(**em_d))
        return qs


class TicketFilter(django_filters.FilterSet):
    """doc string for OrganizationFilter"""

    reference_number = django_filters.CharFilter()
    coverage_type = django_filters.CharFilter()
    repair_type = django_filters.CharFilter()
    customer_contact_number = django_filters.CharFilter(
        field_name="customer__contact_number"
    )
    created_by = UserNameFilter(field_name="created_by")
    organization = django_filters.CharFilter(field_name="organization__code")
    currently_assigned_to_email = django_filters.CharFilter(
        field_name="currently_assigned_to__email"
    )
    device = DeviceFilter(field_name="device")
    customer = CustomerFilter(field_name="customer")
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )

    class Meta(object):
        model = models.Ticket
        exclude = ("unit_part_reports", "customer_signature", "component_issues")


class TicketViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.TicketSerializer
    filter_class = TicketFilter
    permission_classes = [TicketPermissions]
    retrieve_serializer_class = serializers.TicketPrintSerializer
    search_fields = (
        "reference_number",
        "customer__first_name",
        "customer__last_name",
        "customer__contact_number",
    )
    list_serializer_class = serializers.TicketListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.role in [PRIVILEGED]:
                return models.Ticket.objects.all()
            else:
                (organizations, managed_organizations) = self.get_user_organizations()
                return models.Ticket.objects.filter(
                    Q(organization__in=organizations)
                    | Q(organization__in=managed_organizations)
                )
        return models.Ticket.objects.all()

    @decorators.action(
        methods=["get"],
        detail=False,
        url_path="details_by_reference_number/(?P<reference_number>\w+)",
        url_name="details_by_reference_number",
    )
    def details_by_reference_number(self, request, reference_number):
        ticket = models.Ticket.objects.get(reference_number=reference_number)
        context = {"request": request}
        return response.Response(
            self.retrieve_serializer_class(ticket, context=context).data
        )

    @decorators.action(methods=["GET"], detail=True)
    def get_applicable_loaner_devices(self, request, pk=None):
        "Get diagnosis suites for device."

        if pk is not None:
            ticket = models.Ticket.objects.get(pk=pk)
            devices = ticket.organization.get_available_loaner_devices()
            if "search" in request.query_params:
                search_text = request.query_params["search"]
                search_text.strip()
                if search_text:
                    devices = devices.annotate(
                        search=SearchVector(
                            "part_number", "serial_number", "description"
                        )
                    ).filter(search=search_text)

            context = {"request": request}
            return response.Response(
                LoanerItemSerializer(devices, many=True, context=context).data
            )

    @decorators.action(methods=["GET"], detail=True)
    def get_applicable_repair_spares(self, request, pk=None):
        "Get diagnosis suites for device."
        if pk is not None:
            ticket = models.Ticket.objects.get(pk=pk)
            org = ticket.organization

            devices = org.get_available_repair_items()
            if "search" in request.query_params:
                search_text = request.query_params["search"]
                search_text.strip()
                if search_text:
                    devices = devices.annotate(
                        search=SearchVector(
                            "part_number", "serial_number", "description"
                        )
                    ).filter(search=search_text)
            context = {"request": request}
            return response.Response(
                RepairItemSerializer(devices, many=True, context=context).data
            )

    @decorators.action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.TicketStatusChangeSerializer,
        url_name="change_ticket_status",
    )
    def change_status(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        serializer = self.get_serializer_class()(
            ticket, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data["status"] in ["Delivered"]:
                delivery = ticket.delivery
                delivery.device_pickup_time = timezone.now()
                delivery.save()
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        obj = self.get_object()
        data = self.retrieve_serializer_class(obj, context={"request": request}).data
        return response.Response(data, status=status.HTTP_200_OK, headers=headers)

    @decorators.action(
        methods=["post", "get"], detail=True, url_name="send_ticket_details_by_email"
    )
    def send_ticket_details_by_email(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        ticket.send_ticket_details_to_customer_via_email()
        data = self.retrieve_serializer_class(ticket, context={"request": request}).data
        return response.Response(data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=["post", "get"], detail=True, url_name="send_ticket_details_by_sms"
    )
    def send_ticket_details_by_sms(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        ticket.send_ticket_details_to_customer_via_sms()
        data = self.retrieve_serializer_class(ticket, context={"request": request}).data
        return response.Response(data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=["post", "get"], detail=True, url_name="send_ticket_status_by_email"
    )
    def send_ticket_status_by_email(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        ticket.send_ticket_status_update_to_customer_via_email()
        data = self.retrieve_serializer_class(ticket, context={"request": request}).data
        return response.Response(data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=["post", "get"], detail=True, url_name="send_ticket_status_by_sms"
    )
    def send_ticket_status_by_sms(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        ticket.send_ticket_status_update_to_customer_via_sms()
        data = self.retrieve_serializer_class(ticket, context={"request": request}).data
        return response.Response(data, status=status.HTTP_200_OK)

    @decorators.action(methods=["post", "get"], detail=True, url_name="ticket_pdf")
    def pdf(self, request, pk):
        """Generate pdf."""
        ticket = self.get_object()
        html_string = render_to_string("ticket.html", {"ticket": ticket})
        html = HTML(string=html_string)
        margins = "{0}px {1} {2}px {1}".format(10, 10, "1cm")
        content_print_layout = "@page {size: A4 portrait; margin: %s;}" % margins
        result = html.write_pdf(
            stylesheets=[
                CSS(string=content_print_layout),
                os.path.join(settings.STATIC_ROOT, "bootstrap.min.css"),
            ]
        )
        response = HttpResponse(content_type="application/pdf;")
        response["Content-Disposition"] = "inline; filename=list_people.pdf"
        response["Content-Transfer-Encoding"] = "binary"
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, "rb")
            response.write(output.read())
        return response

    @decorators.action(
        methods=["POST"],
        detail=True,
        serializer_class=serializers.UploadContentSerializer,
        parser_classes=[MultiPartParser],
    )
    def upload(self, request, pk=None):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.update(
                {
                    "content_object": ticket,
                    "upload_type": "Ticket",
                    "created_by": request.user,
                }
            )
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        methods=["POST"],
        detail=True,
        url_path="upload_signature/(?P<reference_number>\w+)/(?P<guid>\w+)",
        serializer_class=serializers.TicketSignatureSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def upload_signature(self, request, pk, reference_number, guid):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        if ticket.reference_number == reference_number and ticket.guid == guid:
            serializer = self.get_serializer_class()(
                ticket, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            headers = self.get_success_headers(serializer.data)
            obj = self.get_object()
            data = self.retrieve_serializer_class(
                obj, context={"request": request}
            ).data
            return response.Response(data, status=status.HTTP_200_OK, headers=headers)
        return response.Response("Invalid paramters", status.HTTP_400_BAD_REQUEST)

    @decorators.action(methods=["post", "get"], detail=True, url_name="get_gsx_data")
    def get_gsx_data(self, request, pk):
        "Get diagnosis suites for device."
        ticket = self.get_object()
        gsx_repair_type = ticket.device.gsx_repair_type
        converter = get_convertor_class(gsx_repair_type)
        data = {}
        if converter:
            c = converter(ticket)
            c.convert()
            data = c.data
        else:
            data = {"meta": {"messages": ["No Adeqaute convertor found."]}}
        return response.Response(data, status=status.HTTP_200_OK)
