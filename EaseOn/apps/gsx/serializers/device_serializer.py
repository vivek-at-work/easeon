# -*- coding: utf-8 -*-
import copy

from core.utils import time_by_adding_business_days, is_in_dev_mode
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer
from .gsx_validate import gsx_validate

dummy_response = {"device": {"identifiers": {"serial": "FCGT24E5HFM2", "imei": "359223073482536", "meid": "35922307348253"}, "productDescription": "iPhone 6s Plus", "activationDetails": {"carrierName": "*****", "lastRestoreDate": "1970-01-01T00:00:00Z", "firstActivationDate": "1970-01-01T00:00:00Z", "unlockDate": "1970-01-01T00:00:00Z", "productVersion": "*****", "initialActivationPolicyID": "***", "initialActivationPolicyDetails": "********", "appliedActivationPolicyID": "****", "appliedActivationDetails": "********", "nextTetherPolicyID": "***", "nextTetherPolicyDetails": "********", "productDescription": "IPHONE 6S PLUS SPACE GRAY 32GB-HIN", "lastUnbrickOsBuild": "******"}, "productLine": "*******", "configCode": "*****", "configDescription": "******************************", "soldToName": "************************************",
                             "warrantyInfo": {"warrantyStatusCode": "***", "warrantyStatusDescription": "******************************", "coverageEndDate": "1970-01-01T00:00:00Z", "coverageStartDate": "1970-01-01T00:00:00Z", "daysRemaining": 0, "purchaseDate": "1970-01-01T00:00:00Z", "onsiteStartDate": "1970-01-01T00:00:00Z", "onsiteEndDate": "1970-01-01T00:00:00Z", "purchaseCountry": "****", "registrationDate": "1970-01-01T00:00:00Z", "contractCoverageEndDate": "1970-01-01T00:00:00Z", "contractCoverageStartDate": "1970-01-01T00:00:00Z"}, "caseDetails": [{"caseId": "*************", "createdDateTime": "1970-01-01T00:00:00Z", "summary": "*******"}, {"caseId": "*************", "createdDateTime": "1970-01-01T00:00:00Z", "summary": "*******"}, {"caseId": "*************", "createdDateTime": "1970-01-01T00:00:00Z", "summary": "*******"}]}}


class DeviceSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    identifier = serializers.CharField()

    def validate_identifier(self, value):
        """
        Check that device identifier is valid.
        """
        is_valid_alternate_device_id = gsx_validate(value, "alternateDeviceId")
        is_valid_sn = gsx_validate(value, "serialNumber")
        if not is_valid_alternate_device_id and not is_valid_sn:
            raise serializers.ValidationError(
                "Not a valid serial number or IMEI number."
            )
        return value

    def create(self, validated_data):
        """

        :param validated_data: valid data
        :return: pyotp object
        """
        if is_in_dev_mode():
            return dummy_response
        req = GSXRequest(
            "repair",
            "product/details?activationDetails=true",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {"id": validated_data["identifier"]}
        received_on = time_by_adding_business_days(0).isoformat()
        response = req.post(unitReceivedDateTime=received_on, device=device)
        return response
