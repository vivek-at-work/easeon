import customers
import devices
import organizations
import slas
from core.serializers import BaseMeta, BaseSerializer, UserSerializer
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

class CustomerTicketSerializer(BaseSerializer):

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

        if not obj.is_closed:
            messages.append(
                "Current Status of ticket is {0} it should be one from {1}".format(
                    obj.status, ",".join(models.CLOSE_STATUS_VALUES)
                )
            )

        if not obj.has_consolidated_loaner_items():
            messages.append(
                """Consolidation of loaner Items is Pending.
             Check If Any of the loaner record is not moarked retuned"""
            )

        if not obj.has_consolidated_order_lines():
            messages.append(
                """Consolidation of Order Line Items is Pending.
             Check atleast one OrderLine or serilizable Orderline
             record should exist"""
            )
        if not obj.has_consolidated_gsx_repair_info():
            messages.append(
                """Consolidation of GSX Repair Info is Pending.
             Check atleast one GSX Repair Info
             record should exist"""
            )

        user = self.get_user()
        manager_flag = user.managed_locations.filter(id=obj.organization.id).exists()
        return {"flag": obj.is_closed or manager_flag, "messages": messages}

    class Meta(BaseMeta):
        model = models.Ticket
