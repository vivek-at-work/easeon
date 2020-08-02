# -*- coding: utf-8 -*-
import logging

from core.serializers import (PasswordChangeSerializer,
                              PasswordResetConfirmSerializer,
                              PasswordResetSerializer)
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions, response, status

sensitive_post_parameters_m = method_decorator(  # pylint:disable=C0103
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class PasswordResetView(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.info(
                'Sent password reset link for request data {}'.format(
                    request.data
                )
            )
            return response.Response(
                {
                    'detail': 'Password reset e-mail has been sent to your mail box please follow the same.'
                },
                status=status.HTTP_200_OK,
            )
        except Exception as identifier:
            logging.error(
                'Could not send password reset link for request data {} due to {}'.format(
                    request.data, identifier
                )
            )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.info(
                'password reset done for request data {} '.format(request.data)
            )
            return response.Response(
                {'detail': 'Password has been reset with the new password.'}
            )
        except Exception as identifier:
            logging.error(
                'password reset failed for request data {} due to {} '.format(
                    request.data, identifier
                )
            )
            raise identifier


class PasswordChangeView(generics.GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):  # pylint:disable=W0221
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):  # pylint:disable=W0613
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.info(
                'Password change successfull for request data {} for user {} '.format(
                    request.data, request.user
                )
            )
            return response.Response(
                {'detail': 'New password has been updated.'}
            )
        except Exception as identifier:
            logging.error(
                'password change failed for request data {} for user {} due to {} '.format(
                    request.data, request.user, identifier
                )
            )
            return response.Response(
                {'detail': 'Password change failed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


# def send_password_to_user(self):
#     template = settings.EMAIL_TEMPLATES.get(
#         'send_password_to_user', None)
#     password = self.change_password()
#     if template is not None:
#         details = """Perform day to day
#             usage of the portal the with the shared password {0}."""
#         login_url = "{0}{1}".format(settings.SERVER_IP,
#                                     reverse(
#                                         'rest_login')
#                                     )
#         context = {
#             'receiver_short_name': self.get_short_name(),
#             'summary': """Your account has been varfied by the admin.
#                     with email address {1}.""".format(self.email),
#             'detail': details.format(),
#             'action_link': login_url,
#             'action_name': 'Login'
#         }
#         subject = 'Password for user {0} account'.format(
#             self.username)
#         send_mail(subject, template,
#                   self.email, **context)
