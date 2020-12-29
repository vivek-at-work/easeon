# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from core.utils import get_organization_model, is_in_dev_mode
from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tokens.commands import send_token_display_refresh_command
from tokens.models import Token


class TokenSerializer(BaseSerializer):
    organization_code = serializers.SlugRelatedField(
        read_only=True, slug_field="code", source="organization"
    )
    token_number = serializers.CharField(read_only=True)
    counter_number = serializers.CharField(read_only=True)
    can_invite = serializers.SerializerMethodField()
    invited_by = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail"
    )
    technician_name = serializers.SlugRelatedField(
        read_only=True, slug_field="first_name", source="invited_by"
    )

    def validate(self, data):
        if "view" in self.context:
            action = self.context["view"].action
            if action == "create":
                if (
                    Token.objects.all()
                    .created_between().filter(contact_number=data["contact_number"])
                    .exists()
                ):
                    raise serializers.ValidationError(
                        "You already have a token sent on you number.If Not received in next 2 minutes, Please reach out to reception"
                    )
        return data

    class Meta(BaseMeta):
        model = Token
        fields = (
            "url",
            "first_name",
            "location_code",
            "last_name",
            "token_number",
            "email",
            "organization_code",
            "contact_number",
            "counter_number",
            "invited_by",
            "technician_name",
            "invite_sent_on",
            "can_invite",
            "is_present",
            "category",
        )

    def create(self, validated_data):
        validated_data["created_by"] = get_user_model().objects.first()
        Organization = apps.get_model(*get_organization_model().split(".", 1))
        validated_data["organization"] = Organization.objects.get(
            token_machine_location_code=validated_data["location_code"]
        )
        validated_data["token_number"] = (
            Token.objects.filter(location_code=validated_data["location_code"])
            .created_between()
            .count()
            + 1
        )
        instance = Token.objects.create(**validated_data)
        instance.send_token_number_by_sms()
        if not is_in_dev_mode():
            send_token_display_refresh_command(instance)
        return instance

    def get_can_invite(self, obj):
        requesting_user = self.context["request"].user
        return obj.can_invite(requesting_user)


class InviteCustomerSerializer(serializers.Serializer):
    counter_number = serializers.IntegerField(min_value=1, max_value=50)
