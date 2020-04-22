# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from customers.models import Customer
from django.db import transaction
from lists.models import get_list_choices
from rest_framework import serializers

c_types = get_list_choices('CUSTOMER_TYPE')


class CustomerSerializer(BaseSerializer):
    state = serializers.ChoiceField(choices=get_list_choices('STATES'))
    customer_type = serializers.ChoiceField(choices=c_types)
    country = serializers.ChoiceField(choices=get_list_choices('COUNTRY'))

    class Meta(BaseMeta):
        model = Customer
        read_only_fields = [
            'id',
            'url',
            'created_by',
            'created_at',
            'is_deleted',
            'guid',
            'updated_at',
            'deleted_at',
            'version',
            'last_visit_on',
            'last_modified_by',
        ]

    # def create(self, validated_data):
    #     # TODO: what if address needes to be updated  for next ticket
    #     with transaction.atomic():
    #         email = validated_data['email']
    #         contact_number = validated_data['contact_number']
    #         results = Customer.objects.filter(email=email,
    #                                           contact_number=contact_number)
    #         if results.count() > 0:
    #             return results[0]
    #         else:
    #             return super(CustomerSerializer, self).create(validated_data)
