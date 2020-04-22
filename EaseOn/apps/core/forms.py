# -*- coding: utf-8 -*-
from core.utils import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class CustomPasswordResetForm(PasswordResetForm):
    email_template = settings.EMAIL_TEMPLATES.get('action', None)

    def save(
        self,
        domain_override=None,
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name=email_template,
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data['email']
        super(CustomPasswordResetForm, self).get_users(email)
        for user in get_user_model().objects.filter(
            email=email, is_active=True
        ):
            user.send_reset_password_link()
