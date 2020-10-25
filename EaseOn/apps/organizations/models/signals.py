# -*- coding: utf-8 -*-
from django.dispatch import Signal

args = ["membership", "attributes"]
membership_attributes_changed = Signal(providing_args=args)
