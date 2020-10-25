# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

from core import views
from core.router import DefaultRouter
from core.views import (
    AdminAccountApprove,
    EmailVerificationView,
    LoginViewSet,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    PingPongView,
    RegistrationView,
    UserEmailTakenView,
)
from core.viewsets import UserViewSet
from django.conf.urls import url

UUID_REGEX = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


otp_options = LoginViewSet.as_view({"post": "get_otp_options"})
generate_otp = LoginViewSet.as_view({"post": "generate_otp"})
verify_otp = LoginViewSet.as_view({"post": "verify_otp"})
refresh_token = LoginViewSet.as_view({"post": "refresh_token"})


core_router = DefaultRouter()
core_router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    # URLs that do not require a session or valid token
    url(r"ping", PingPongView.as_view(), name="ping"),
    url(r"otp_options", otp_options, name="otp-options"),
    url(r"generate_otp", generate_otp, name="generate-otp"),
    url(
        r"^verify_otp/(?P<uuid>{uuid})/$".format(uuid=UUID_REGEX),
        verify_otp,
        name="verify-otp",
    ),
    url(r"^refresh_token", refresh_token, name="refresh_token"),
    url(r"^register/$", RegistrationView.as_view(), name="register"),
    url(r"^logout/$", LogoutView.as_view(), name="rest_logout"),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="rest_password_reset"),
    url(
        r"^password/reset/confirm/$",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    url(
        r"^user_email_verification",
        EmailVerificationView.as_view(),
        name="user_email_verification",
    ),
    url(
        r"^user_account_approve",
        AdminAccountApprove.as_view(),
        name="user_account_approve",
    ),
    url(r"^register/email_taken/$", UserEmailTakenView.as_view(), name="email_taken"),
    url(
        r"^password_change/$",
        PasswordChangeView.as_view(),
        name="authenticated_user_password_change",
    ),
    # url(
    #     r'^configurations/$',
    #     ApplicationDetailsView.as_view(),
    #     name='configurations',
    # ),
]
