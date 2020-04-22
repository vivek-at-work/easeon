# -*- coding: utf-8 -*-
""" Serializer for Service Provider Membership Models"""
from core.serializers import BaseSerializer
from organizations.models import OrganizationRights
from rest_framework import serializers


class OrganizationRightsSerializer(BaseSerializer):
    is_active = serializers.ReadOnlyField()
    organization_code = serializers.SlugRelatedField(
        read_only=True, slug_field='code', source='organization'
    )
    organization_name = serializers.SlugRelatedField(
        read_only=True, slug_field='name', source='organization'
    )
    can_toggle_status = serializers.SerializerMethodField()

    def validate_user(self, value):
        """
        Check that user is nor the super user  or manager  for organization
        """
        # if value.is_superuser:
        #     raise serializers.ValidationError(
        #         'Can not create/update membership for a superuser.'
        #     )
        if not self.get_user().is_superuser and value != self.get_user():
            raise serializers.ValidationError(
                'Can not create/update membership for other users.'
            )
        return value

    def get_can_toggle_status(self, obj):
        return (
            self.get_user().is_superuser
            or obj.organization.manager == self.get_user()
        )

    # def validate_uniques(self,data,key,value):
    #     d = {key:value}
    #     if not self.instance:
    #         if Organization.objects.all().filter(**d).exists():
    #             raise serializers.ValidationError("{0} Already been used with previous existing organization.".format(key))
    #     else:
    #         if Organization.objects.exclude(id=self.instance.id).filter(**d).exists():
    #             raise serializers.ValidationError("{0} Already been used with previous existing organization.".format(key))

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['organization'] in data['user'].managed_locations.all():
            raise serializers.ValidationError(
                """
        Can not  assign rights for the user {} as user is assigned as manager
        for organization {}
        """.format(
                    data['user'], data['organization']
                )
            )
        if not self.instance:
            if (
                data['user']
                .locations.filter(organization=data['organization'])
                .count()
                > 0
            ):
                raise serializers.ValidationError(
                    """
            Can not assign rights for the user {} as user has already been added
            for organization {}
            """.format(
                        data['user'], data['organization']
                    )
                )

        # if not (data["tickets"] and data["repair_inventory"]
        #          and data["loaner_inventory"] and data["serializable_inventory"]
        #          and data["daily_status_report_download"] and data["customer_info_download"]
        #         and data["daily_status_report_download_with_customer_info"]):
        #     raise serializers.ValidationError(
        #         "Provide some rights to the user for this membership.")

        if data['user'].is_superuser:
            data['is_active'] = True
        return data

    class Meta(object):
        model = OrganizationRights
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
        fields = [
            'url',
            'user',
            'organization',
            'tickets',
            'repair_inventory',
            'loaner_inventory',
            'non_serialized_inventory',
            'daily_status_report_download',
            'daily_status_report_download_with_customer_info',
            'customer_info_download',
            'is_active',
            'organization_code',
            'can_toggle_status',
            'organization_name',
        ]
