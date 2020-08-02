# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

import logging

from core.permissions import IsOperatorOrSuperUser
from gsx import serializers
from rest_framework import permissions, response, status, viewsets
from rest_framework.permissions import AllowAny


class GSXViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializers_dict = {
        'warranty': serializers.DeviceSerializer,
        'diagnostic_suites': serializers.DiagnosticSuitesSerializer,
        'repair_eligibility': serializers.RepairEligibilitySerializer,
        'diagnostics_lookup': serializers.DiagnosticsLookupSerializer,
        'run_diagnosis_suite': serializers.RunDiagnosticsSerializer,
        'diagnostics_status': serializers.DiagnosticsStatusSerializer,
    }

    def get_serializer_class(self):
        return self.serializers_dict.get(
            self.action, serializers.NoneSerializer
        )

    def _validate(self, serializer, data):
        """
        :param serializer: serializer against which data to ve validated
        :param data: data to ve validated
        :return: serializer instance.
        """

        serializer_instance = serializer(
            data=data, context={'request': self.request}
        )
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()

    def warranty(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)

    def diagnostic_suites(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)

    def repair_eligibility(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)

    def diagnostics_lookup(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)

    def run_diagnosis_suite(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)

    def diagnostics_status(self, request):
        """
        """
        serializer = self.get_serializer_class()
        serializer = self._validate(serializer, request.data)
        return response.Response(serializer, status=status.HTTP_201_CREATED)
