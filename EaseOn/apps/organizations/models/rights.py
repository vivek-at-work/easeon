# -*- coding: utf-8 -*-
from core import utils
from core.models import BaseModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .signals import membership_attributes_changed


class OrganizationRights(BaseModel):
    organization = models.ForeignKey(
        utils.get_organization_model(),
        on_delete=models.DO_NOTHING,
        related_name='memberships',
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='locations'
    )
    repair_inventory = models.BooleanField(default=False)
    loaner_inventory = models.BooleanField(default=False)
    non_serialized_inventory = models.BooleanField(default=False)
    tickets = models.BooleanField(default=False)
    daily_status_report_download = models.BooleanField(default=False)
    daily_status_report_download_with_customer_info = models.BooleanField(
        default=False
    )
    customer_info_download = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['organization', 'user'],
                condition=Q(is_deleted=False),
                name='membership_unique_is_deleted',
            )
        ]

    def toggle_activation(self, is_active):
        self.is_active = is_active
        self.save()
        membership_attributes_changed.send(
            sender=self.__class__, membership=self, attributes=['is_active']
        )


@receiver(post_save, sender=OrganizationRights)
def onMembershipSave(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        template = settings.EMAIL_TEMPLATES.get('alert')
        details = """A new Rights request received from user {} for organization {} please login to approve""".format(
            instance.user.full_name, instance.organization.code
        )

        summary = """New Right approval request received for  {0}.""".format(
            settings.SITE_HEADER
        )
        context = {
            'receiver_short_name': 'Admin',
            'summary': summary,
            'detail': details,
            'action_name': 'View',
        }
        subject = summary
        receivers = get_user_model().objects.all_superusers_email()
        receivers_emails = []
        for r in receivers:
            receivers_emails.append(r)
        receivers_emails.append(instance.user.email)
        utils.send_mail(subject, template, *(receivers_emails), **context)


@receiver(membership_attributes_changed)
def method_to_do_stuff(sender, membership, attributes, **kwargs):
    if 'is_active' in attributes and getattr(membership, 'is_active'):
        template = settings.EMAIL_TEMPLATES.get('action', None)
        subject = 'Your Membership request has been approved'.format(
            settings.SITE_HEADER
        )
        summary = """Your Membership request has been approved."""
        details = """Please click on the link bellow to login."""
        action_name = 'Login'
        login_url = '{0}'.format(settings.SERVER_IP)
        context = {
            'receiver_short_name': membership.user.get_short_name(),
            'summary': summary,
            'detail': details.format(),
            'action_name': action_name,
            'action_link': login_url,
        }
        utils.send_mail(subject, template, membership.user.email, **context)

    if 'is_active' in attributes and not getattr(membership, 'is_active'):
        template = settings.EMAIL_TEMPLATES.get('alert', None)
        subject = 'Your Membership  has been deactivate'.format(
            settings.SITE_HEADER
        )
        summary = """Your Membership has been deactivate by the admin."""
        context = {
            'receiver_short_name': membership.user.get_short_name(),
            'summary': summary,
        }
        utils.send_mail(subject, template, membership.user.email, **context)
