# -*- coding: utf-8 -*-
from core.utils import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .device import Device
