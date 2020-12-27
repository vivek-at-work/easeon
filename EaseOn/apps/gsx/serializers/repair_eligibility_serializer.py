# -*- coding: utf-8 -*-
import copy

from core.utils import time_by_adding_business_days, is_in_dev_mode
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer
from .gsx_validate import gsx_validate
dummy_response = {"eligibilityDetails": {"outcome": [{"action": "WARNING", "reasons": [{"type": "WARNING", "messages": ["Find My Device is active. Find My Device must be turned off for non-accessory repairs. See OP1395 for details."]}]}, {"reasons": [{"type": "REPAIR_TYPE", "messages": [
    "MRI or Serial Number Reader diagnostics are required to proceed with a repair."], "repairOptions":[{"option": "SVNR", "priority": 1, "subOption": "NTF"}, {"option": "SVNR", "priority": 2, "subOption": "SRC"}]}]}], "coverageCode": "OO", "coverageDescription": "Out Of Warranty (No Coverage)", "technicianMandatory": False}}


class RepairEligibilitySerializer(BaseGSXSerializer):
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
        if is_in_dev_mode():
            return dummy_response
        req = GSXRequest(
            "repair",
            "eligibility",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        device = {"id": validated_data["identifier"]}
        response = req.post(device=device)
        return response
