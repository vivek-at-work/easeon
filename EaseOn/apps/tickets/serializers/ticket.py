# -*- coding: utf-8 -*-
import customers
import devices
import organizations
import slas
from core.serializers import (
    BaseMeta,
    BaseSerializer,
    FileFieldWithLinkRepresentation,
    UserSerializer,
)
from core.utils import time_by_adding_business_days
from core.permissions import SUPER_USER,PRIVILEGED
from devices.serializers import ComponentIssueSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from lists.models import get_list_choices
from rest_framework import serializers
from tickets import models
from tickets import serializers as t_serializer

from .device_part_report import DevicePartReportSerializer
from .gsx_info import GSXInfoSerializer
from .upload_content_serializer import UploadContentSerializer
from .voucher import VoucherSerializer


def device_do_not_have_open_tickets(device):
    if not device.is_exempted_device and device.open_tickets.count():
        raise serializers.ValidationError("Device has previous open tickets.")


def customer_do_not_have_open_tickets(customer):
    if not settings.ENABLE_MULTIPLE_TICKETS_FOR_CUSTOMER:
        if customer.open_tickets.count():
            raise serializers.ValidationError("Customer has previous open tickets.")


class TicketListSerializer(BaseSerializer):
    device_id = serializers.SlugRelatedField(
        source="device", read_only=True, slug_field="serial_number"
    )
    gsx_ship_to = serializers.SlugRelatedField(
        source="organization", read_only=True, slug_field="gsx_ship_to"
    )

    class Meta(BaseMeta):
        model = models.Ticket
        fields = [
            "id",
            "url",
            "inward_time",
            "created_at",
            "is_deleted",
            "reference_number",
            "closed_on",
            "closed_by",
            "organization",
            "repair_type",
            "status",
            "coverage_type",
            "gsx_ship_to",
            "device_id",
        ]
        c_u_d = serializers.CurrentUserDefault
        extra_kwargs = {
            "created_by": {"default": c_u_d()},
            "currently_assigned_to": {"default": c_u_d()},
        }


class TicketSerializer(BaseSerializer):
    """
    Used in Post/and put  requests
    """

    def validate(self, values):
        if (
            "organization" in values
            and "expected_delivery_time" in values
            and values["organization"]
            .holidays.filter(date=values["expected_delivery_time"].date())
            .exists()
        ):
            raise serializers.ValidationError("Not a valid Expected delivery date.")
        return values

    device = serializers.HyperlinkedRelatedField(
        queryset=devices.models.Device.objects,
        view_name="device-detail",
        validators=[device_do_not_have_open_tickets],
    )

    customer = serializers.HyperlinkedRelatedField(
        queryset=customers.models.Customer.objects,
        view_name="customer-detail",
        validators=[customer_do_not_have_open_tickets],
    )

    uploaded_contents = UploadContentSerializer(many=True, read_only=True)

    sla = serializers.HyperlinkedRelatedField(
        queryset=slas.models.SLA.objects, view_name="sla-detail"
    )

    delivery = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="delivery-detail"
    )

    reference_number = serializers.CharField(read_only=True)
    unit_part_reports = serializers.JSONField(
        required=False, initial=dict, allow_null=True
    )
    password = serializers.CharField(read_only=True)
    customer_signature = FileFieldWithLinkRepresentation(read_only=True)
    status = serializers.ChoiceField(
        default="Registered", choices=get_list_choices("TICKET_STATUS")
    )
    repair_type = serializers.ChoiceField(choices=get_list_choices("REPAIR_TYPE"))
    comments = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="comment-detail"
    )
    vouchers = serializers.HyperlinkedRelatedField(
        view_name="voucher-detail", many=True, read_only=True
    )
    loaner_records = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="loanerrecord-detail"
    )
    serializable_order_lines = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="serializableorderline-detail"
    )
    currently_assigned_to = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects,
        view_name="user-detail",
        default=serializers.CurrentUserDefault(),
    )
    currently_assigned_to_name = serializers.SlugRelatedField(
        source="currently_assigned_to", read_only=True, slug_field="full_name"
    )
    first_escalation_after = serializers.DateTimeField(
        default=time_by_adding_business_days(2)
    )
    second_escalation_after = serializers.DateTimeField(
        default=time_by_adding_business_days(3)
    )
    final_escalation_after = serializers.DateTimeField(
        default=time_by_adding_business_days(30)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get("context", None)
        if context:
            request = kwargs["context"]["request"]
            queryset = organizations.models.Organization.objects.filter(
                id__in=request.user.locations.filter(
                    tickets=True, is_active=True
                ).values_list("organization", flat=True)
            )
            queryset = organizations.models.Organization.objects.all()
            self.fields["organization"] = serializers.HyperlinkedRelatedField(
                queryset=queryset, view_name="organization-detail"
            )

            if request.method == "PUT":
                self.fields["device"] = serializers.HyperlinkedRelatedField(
                    queryset=devices.models.Device.objects, view_name="device-detail"
                )
                self.fields["customer"] = serializers.HyperlinkedRelatedField(
                    queryset=customers.models.Customer.objects,
                    view_name="customer-detail",
                )

    class Meta(BaseMeta):
        model = models.Ticket
        read_only_fields = [
            "id",
            "url",
            "created_by",
            "created_at",
            "is_deleted",
            "delivery",
            "reference_number",
            "guid",
            "updated_at",
            "deleted_at",
            "version",
            "first_escalation_after",
            "second_escalation_after",
            "vouchers",
            "comments",
            "serializable_order_lines",
            "closed_on",
            "closed_by",
            "last_modified_by",
            "subscribers",
            "currently_assigned_to_name",
        ]
        c_u_d = serializers.CurrentUserDefault
        extra_kwargs = {
            "created_by": {"default": c_u_d()},
            "currently_assigned_to": {"default": c_u_d()},
        }


class DeviceSerializer(BaseSerializer):
    identifier = serializers.CharField()
    product_name = serializers.ReadOnlyField()
    configuration = serializers.ReadOnlyField()
    component_issues = ComponentIssueSerializer(many=True)

    class Meta(BaseMeta):
        model = devices.models.Device
        fields = [
            "url",
            "product_name",
            "configuration",
            "identifier",
            "serial_number",
            "alternate_device_id",
            "component_issues",
        ]


class TicketPrintSerializer(BaseSerializer):

    organization = organizations.serializers.OrganizationSerializer()
    device = DeviceSerializer(read_only=True)
    customer = customers.serializers.CustomerSerializer()
    sla = slas.serializers.SLASerializer()
    delivery = t_serializer.DeliverySerializer(read_only=True)

    reference_number = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(choices=get_list_choices("TICKET_STATUS"))

    device_part_reports = DevicePartReportSerializer(many=True)
    comments = t_serializer.CommentSerializer(many=True)
    vouchers = VoucherSerializer(many=True)
    loaner_records = t_serializer.LoanerRecordSerializer(many=True)
    order_lines = t_serializer.OrderLineSerializer(many=True)
    serializable_order_lines = t_serializer.SerializableOrderLineSerializer(many=True)
    gsx_informations = GSXInfoSerializer(many=True)
    uploaded_contents = UploadContentSerializer(many=True, read_only=True)
    can_update_ticket = serializers.SerializerMethodField()
    can_print_delivery_report = serializers.SerializerMethodField()
    currently_assigned_to_name = serializers.SlugRelatedField(
        source="currently_assigned_to", read_only=True, slug_field="full_name"
    )

    def get_can_update_ticket(self, obj):
        status_flag = not obj.is_closed
        return (
            status_flag
            or self.get_user().is_superuser
            or (obj.organization in self.get_user().managed_locations.all())
        )

    def get_can_print_delivery_report(self, obj):
        messages = []
        has_delivery = False
        try:
            has_delivery = obj.delivery is not None
        except models.Delivery.DoesNotExist:
            messages.append("There is no delivery Infomation Updated")
            return {"flag": has_delivery, "messages": messages}
        if obj.closed_on is None:
            messages.append(
                "Ticket Closed on time is not updated chnage status to any of {} to update it" .format(",".join(models.CLOSED_STATUS_VALUES)
                )
            )

        if not obj.is_delivered:
            messages.append(
                "Current Status of ticket is {0} it should be one from {1}".format(
                    obj.status, ",".join(models.DELIVERED_STATUS_VALUES)
                )
            )

        if not obj.has_consolidated_loaner_items():
            messages.append(
                """Consolidation of loaner Items is Pending.
             Check If Any of the loaner record is not marked returned"""
            )

        if not obj.has_consolidated_order_lines():
            messages.append(
                """Consolidation of Order Line Items is Pending.
             Check at least one OrderLine or serializable Orderline
             record should exist"""
            )
        if not obj.has_consolidated_gsx_repair_info():
            messages.append(
                """Consolidation of GSX Repair Info is Pending.
             Check at least one GSX Repair Info
             record should exist"""
            )
        return {"flag": False if len(messages) > 0 else True, "messages": messages}

    class Meta(BaseMeta):
        model = models.Ticket


class TicketStatusChangeSerializer(BaseSerializer):
    def validate_status(self, value):
        user = self.get_user()
        if user.role == SUPER_USER or user.role == PRIVILEGED or user == self.instance.manager:
            return value

        if (
            self.instance
            and value in ["Delivered"]
            
        ):
            if not hasattr(self.instance, "delivery"):
                raise serializers.ValidationError(
                "Can not change status to delivered unless delivery infomation is updated")
            
            if obj.closed_on is None:
                    raise serializers.ValidationError(
                    "Can not change status to delivered unless ticket is marked closed.")

        


        return value

    status = serializers.ChoiceField(choices=get_list_choices("TICKET_STATUS"))
    delivering_now = serializers.BooleanField(required=False,initial=False)

    class Meta(BaseMeta):
        model = models.Ticket
