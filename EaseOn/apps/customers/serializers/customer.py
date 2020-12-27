# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from customers.models import Customer
from customers.validators import validate_open_tickets
from django.conf import settings
from django.db import transaction
from lists.models import get_list_choices
from rest_framework import serializers

c_types = get_list_choices("CUSTOMER_TYPE")


class CustomerSerializer(BaseSerializer):
    state = serializers.ChoiceField(choices=get_list_choices("STATES"))
    customer_type = serializers.ChoiceField(choices=c_types)
    country = serializers.ChoiceField(choices=get_list_choices("COUNTRY"))

    def validate(self, data):
        if "view" in self.context:
            action = self.context["view"].action
            if action == "create" and not settings.ENABLE_MULTIPLE_TICKETS_FOR_CUSTOMER:
                validate_open_tickets(data)
        return data

    class Meta(BaseMeta):
        model = Customer
        fields = [
            "url",
            "state",
            "customer_type",
            "country",
            "first_name",
            "last_name",
            "city",
            "address_line_1",
            "address_line_2",
            "street",
            "email",
            "contact_number",
            "alternate_contact_number",
            "last_visit_on",
            "pin_code",
            "token_number",
            "user_messages",
        ]