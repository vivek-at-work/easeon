# -*- coding: utf-8 -*-
# from core.serializers import ApplicationSerializer
# from django.conf import settings
# from rest_framework import permissions, status, views
# from rest_framework.response import Response


# class ApplicationDetailsView(views.APIView):
#     """Application settings view."""

#     permission_classes = (permissions.AllowAny,)

#     def get(self, request):  # pylint:disable=R0201
#         'Get application settings.'
#         serializer_class = ApplicationSerializer
#         data = {}
#         data['header'] = settings.SITE_HEADER
#         data['rest_end_point'] = settings.CURRENT_API_URL
#         data['logout_on_password_change'] = settings.LOGOUT_ON_PASSWORD_CHANGE
#         data['is_maintenance_mode_on'] = settings.DEBUG
#         serializer = serializer_class(
#             instance=data, context={'request': request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
