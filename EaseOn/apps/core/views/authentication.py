# -*- coding: utf-8 -*-
import logging
import time

from core import serializers
from core.permissions import IsSuperUser
from core.utils import account_activation_token, default_create_token, send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.utils import encoding, http
from django.utils.translation import ugettext_lazy as _
from rest_framework import decorators, generics, permissions, response, status, views
from rest_framework.authtoken.models import Token as TokenModel
from rest_framework.reverse import reverse_lazy


class LogoutView(generics.GenericAPIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Handle POST Request"""
        try:
            if request.user.is_authenticated:
                request.user.auth_token.delete()
            logging.info("user {}  had been logged out.".format(request.user))
            return response.Response(
                {"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logging.error(
                "user {}  could not be been logged out due to {}.".format(
                    request.user, e
                )
            )
            return response.Response(
                {"detail": _("Could not logged out.")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegistrationView(generics.GenericAPIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SignUpSerializer

    def post(self, request, *args, **kwargs):
        request.data["username"] = "user" + str(time.time())
        logging.info("SignUp Request Received with payload {}.".format(request.data))
        self.serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        logging.info("SignUp Request Received and validated payload successfully.")
        user = self.serializer.save()
        logging.info("User Object created {}.".format(user))
        user.set_unusable_password()
        logging.info(
            " Other users exists so setting non readable password for user {} and won't mark him as Super User.".format(
                user
            )
        )
        try:
            user.save()
        except Exception as e:
            logging.error(
                "Could not save user {} after password change due to {}".format(user, e)
            )

        try:
            user.send_email_verification_mail()
        except Exception as e:
            logging.error(
                "Could not send email validation to  user {} after password change due to {}".format(
                    user, e
                )
            )

        data = self.serializer_class(user, context={"request": request}).data
        data[
            "message"
        ] = "Your Registration was successful .Please Check your email for further instructions."
        return response.Response(data, status=status.HTTP_200_OK)


class UserEmailTakenView(generics.GenericAPIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        data = {"email_available_flag": False, "valid_email": False}
        valid_email = True
        if not email:
            data = {
                "email_available_flag": False,
                "message": "Email to check is not provided.",
                "valid_email": False,
            }
            return response.Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            logging.info(
                "Request received to check if email is taken or not for {}".format(
                    email
                )
            )
            count = get_user_model().objects.filter(email__iexact=email).count()
            data = {"email_available_flag": False, "valid_email": valid_email}
            if count > 0:
                data["message"] = "Email already taken."
                data["email_available_flag"] = False
                logging.warning(
                    "Request received to check if email is taken or not for {} results to not available.".format(
                        email
                    )
                )
            else:
                data["message"] = "Email is available."
                data["email_available_flag"] = True
                logging.info(
                    "Request received to check if email is taken or not for {} results to available".format(
                        email
                    )
                )
            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {"email_available_flag": False, "valid_email": False}
            logging.error(
                "Could not check if email is taken or not due to {}".format(e)
            )
            return response.Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailVerificationView(generics.GenericAPIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle POST Request"""
        try:
            uid = request.data["uid"]
            token = request.data["token"]
            userid = encoding.force_text(http.urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=userid)
            result = account_activation_token.check_token(user, token)
            if result:
                logging.info("Email verification succeeded for user {} ".format(user))
                if user.is_superuser:

                    user.toggle_activation(True)
                    logging.info(
                        "Email verification succeeded for user {} and being admin marked him active ".format(
                            user
                        )
                    )
                    return response.Response(
                        {
                            "flag": result,
                            "detail": _(
                                "Thanks !! Your email has been verified . Please continue with default login password."
                            ),
                        },
                        status=status.HTTP_200_OK,
                    )

                receivers = user.send_email_verification_mail_to_admin(
                    result, send_email=True
                )
                logging.info(
                    "Admins {} has been send mail for user {} to approve.".format(
                        receivers, user
                    )
                )
                return response.Response(
                    {
                        "flag": result,
                        "detail": _(
                            "Your email has been verified. Please check with admin."
                        ),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return response.Response(
                    {
                        "flag": result,
                        "detail": _(
                            "Your email has not been verified. Please Check with admin."
                        ),
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            logging.error("Could not validate user {} email due to {}.".format(user, e))


class AdminAccountApprove(views.APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if get_user_model().objects.all_superusers().count() > 0:
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        """Handle POST Request"""
        try:
            uid = request.data["uid"]
            token = request.data["token"]
            userid = encoding.force_text(http.urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=userid)
            result = account_activation_token.check_token(user, token)
            if result:
                user.toggle_activation(True)
                logging.info(
                    "user {}  had been set active for admin approve by {}.".format(
                        user, request.user
                    )
                )
                return response.Response(
                    {
                        "flag": result,
                        "detail": _(
                            "User Account have been approved for performing actions."
                        ),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return response.Response(
                    {
                        "flag": result,
                        "detail": _(
                            "Invlid Token found while  performing user account approval."
                        ),
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as exception:
            logging.info(
                "could not set user {}  active for after admin approve by {} due to {}.".format(
                    user, request.user, exception
                )
            )
