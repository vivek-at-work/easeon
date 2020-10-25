# -*- coding: utf-8 -*-
import logging

from core.utils import account_activation_token, send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse
from django.utils import encoding, http, timezone

logger = logging.getLogger(__name__)


def verify_email_and_request_account_approval_from_admin(request, uid, token):
    try:
        userid = encoding.force_text(http.urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=userid)
        template = settings.EMAIL_TEMPLATES.get("action", None)
        details = """If you wish to allow this user to perform day to day
        usage of {0} portal then please click on the link bellow.""".format(
            settings.SITE_HEADER
        )
        admin_account_approval_url = "{0}{1}".format(
            settings.SERVER_IP,
            reverse(
                "account_approval_from_admin_done",
                kwargs={"uid": str(uid), "token": str(token)},
            ),
        )
        context = {
            "receiver_short_name": user.get_short_name(),
            "summary": """Please confirm account of user {0}
                with email address {1} by clicking the link below.""".format(
                user.full_name, user.email
            ),
            "detail": details.format(),
            "action_name": "Approve",
            "action_link": admin_account_approval_url,
        }
        subject = "Account Approval for user {0} account".format(user.username)
        admin_mail = settings.ADMIN_EMAIL
        context.update({"admin_email": admin_mail})
        if account_activation_token.check_token(user, token):
            user.is_email_verified_by_user = True
            user.account_activation_mail_sent_to_admin = timezone.now()
            user.save()
            send_mail(subject, template, admin_mail, **context)
            return render(request, "account_activation_success.html", context)
        else:
            return render(request, "account_activation_failure.html", context)
    except Exception as e:
        logger.error("Could not varify user email {0}".format(e))
        context = {"admin_email": admin_mail}
        return render(request, "account_activation_failure.html", context)


def account_approval_from_admin_done(request, uid, token):
    try:
        user_id = encoding.force_text(http.urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=user_id)
        context = {"user_full_name": user.full_name, "user_email": user.email}
        template = "account_activation_done_success.html"
        if account_activation_token.check_token(user, token):
            user.toggle_activation(True)
            return render(request, template, context)
        else:
            return render(request, template, context)
    except Exception as e:
        logger.error("Admin could not approve user email {0}".format(e))
        return render(request, "account_activation_done_failure.html", context)
