# -*- coding: utf-8 -*-
from core.serializers import BaseMeta, BaseSerializer
from lists.models import get_list_choices
from organizations.models import Organization
from rest_framework import serializers
from rest_framework import validators as RV


class OrganizationSerializer(BaseSerializer):
    state = serializers.ChoiceField(choices=get_list_choices('STATES'))
    country = serializers.ChoiceField(choices=get_list_choices('COUNTRY'))
    manager_name = serializers.CharField(
        source='manager.first_name', read_only=True
    )

    def validate_uniques(self, key, value):
        d = {key: value}
        if not self.instance:
            if Organization.objects.all().filter(**d).exists():
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing organization.'.format(
                        key
                    )
                )
        else:
            if (
                Organization.objects.exclude(id=self.instance.id)
                .filter(**d)
                .exists()
            ):
                raise serializers.ValidationError(
                    '{0} Already been used with previous existing organization.'.format(
                        key
                    )
                )

    def validate_email(self, value):
        self.validate_uniques('email', value)
        return value

    def validate_contact_number(self, value):
        self.validate_uniques('contact_number', value)
        return value

    def validate_token_machine_location_code(self, value):
        self.validate_uniques('token_machine_location_code', value)
        return value

    def validate_code(self, value):
        self.validate_uniques('code', value)
        return value

    def validate_manager(self, value):
        """
        Check that user is not a super user.
        """
        if (
            self.instance
            and value.locations.filter(
                organization=self.instance, is_active=True
            ).exists()
        ):
            raise serializers.ValidationError(
                'Can not make a user manager for organization who has active rights with the organization, disable rights  if needed so.'
            )
        return value

    class Meta(BaseMeta):
        model = Organization
        fields = (
            'url',
            'created_by',
            'id',
            'created_at',
            'is_deleted',
            'state',
            'country',
            'manager_name',
            'guid',
            'name',
            'address',
            'pin_code',
            'city',
            'token_machine_location_code',
            'email',
            'contact_number',
            'timings',
            'code',
            'gsx_ship_to',
            'last_modified_by',
            'manager',
        )
