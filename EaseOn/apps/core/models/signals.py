# -*- coding: utf-8 -*-
from django.dispatch import Signal

user_attributes_changed = Signal(providing_args=['user', 'attributes'])
