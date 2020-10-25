# -*- coding: utf-8 -*-
"""
View For Ticket related Operations
"""
import django_filters
from core import viewsets
from core.permissions import HasManagerRightsToUpdateOrDelete
from devices.validators import gsx_validate
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from inventory.serializers import LoanerItemSerializer, RepairItemSerializer
from rest_framework import decorators, response, status
from rest_framework.parsers import MultiPartParser
from tickets import models, serializers


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
            em_d = {f"{self.field_name}__email": value}
            return qs.filter(Q(**cn_d) | Q(**em_d))
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
        exclude = ()


class TicketViewSet(viewsets.BaseViewSet):
    serializer_class = serializers.TicketSerializer
    filter_class = TicketFilter
    permission_classes = [HasManagerRightsToUpdateOrDelete]
    retrieve_serializer_class = serializers.TicketPrintSerializer
    search_fields = (
        "reference_number",
        "customer__first_name",
        "customer__last_name",
        "customer__contact_number",
    )
    list_serializer_class = serializers.TicketListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Ticket.objects.all()
        else:
            (organizations, managed_organizations) = self.get_user_organizations()
            return models.Ticket.objects.filter(
                Q(organization__in=organizations)
                | Q(organization__in=managed_organizations)
            )

    # @decorators.action(methods=['GET'], detail=True)
    # def details_by_reference_number(self, request, pk=None):
    #     ticket = self.get_object()
    #     context = {'ticket': ticket}
    #     html_template = get_template('ticket.html').render(context)
    #     return HttpResponse(
    #         html_template, content_type='application/xhtml+xml'
    #     )
    #     # pdf_file = HTML(string=html_template).write_pdf()
    #     # response = HttpResponse(pdf_file, content_type='application/pdf')
    #     # response['Content-Disposition'] = 'filename="ticket-{0}.pdf"'.format(str(ticket))
    #     return response

    @decorators.action(
        methods=["get"],
        detail=False,
        url_path="details_by_reference_number/(?P<reference_number>\w+)",
        url_name="details_by_reference_number",
    )
    def details_by_reference_number(self, request, reference_number):
        # Do something
        ticket = models.Ticket.objects.get(reference_number=reference_number)
        context = {"request": request}
        return response.Response(
            self.retrieve_serializer_class(ticket, context=context).data
        )

    @decorators.action(methods=["GET"], detail=True)
    def pdf(self, request, pk=None):
        ticket = self.get_object()
        context = {"ticket": ticket}
        html_template = get_template("ticket.html").render(context)
        return HttpResponse(html_template, content_type="application/xhtml+xml")
        # pdf_file = HTML(string=html_template).write_pdf()
        # response = HttpResponse(pdf_file, content_type='application/pdf')
        # response['Content-Disposition'] = 'filename="ticket-{0}.pdf"'.format(str(ticket))
        return response

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

    @decorators.action(methods=["GET"], detail=True)
    def create_GSX_repair(self, request, pk=None):
        "Get diagnosis suites for device."
        if pk is not None:
            ticket = self.get_object()
            suites = ticket.create_gsx_reapir(request.user.gsx_auth_token)
            return response.Response(suites)

    @decorators.action(methods=["GET"], detail=True)
    def get_device_questions(self, request, pk=None):
        "Get diagnosis suites for device."
        if pk is not None:
            ticket = self.get_object()
            device = ticket.device
            questions = device.get_repair_questions(request.user.gsx_auth_token)
            return response.Response(questions)

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
