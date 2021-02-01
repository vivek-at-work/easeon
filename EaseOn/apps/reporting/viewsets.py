# -*- coding: utf-8 -*-
import os

from core.viewsets import BaseViewSet
from django.http import HttpResponse
from reporting import models, permissions, serializers,convertors
from rest_framework import renderers, response
from rest_framework.decorators import action



class PassthroughRenderer(renderers.BaseRenderer):
    """
    Return data as-is. View should supply a Response.
    """

    media_type = ""
    format = ""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ReportsViewSet(BaseViewSet):
    queryset = models.ReportRequest.objects
    serializer_class = serializers.ReportRequestSerializer

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[permissions.HasReportDownloadPermissions],
        renderer_classes=(PassthroughRenderer,),
    )
    def download(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = open(instance.final_report_path, "rb")
        response = HttpResponse(file_handle, content_type="application/octet-stream")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="%s"' % os.path.basename(file_handle.name)
        return response

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[permissions.HasReportDownloadPermissions],
        renderer_classes=(PassthroughRenderer,),
    )
    def download_excel(self, *args, **kwargs):
        instance = self.get_object()
        csv_to_xlsx_path = convertors.csv_to_xlsx(instance.final_report_path)
        file_handle = open(csv_to_xlsx_path, "rb")
        response = HttpResponse(file_handle, content_type="application/octet-stream")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="%s"' % os.path.basename(file_handle.name)
        return response

    @action(methods=["post"], detail=True)
    def run(self, *args, **kwargs):
        instance = self.get_object()
        instance.process()
        return response.Response(
            self.serializer_class(instance, context={"request": self.request}).data
        )
