# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.admin import register
from customers import models

register(models.Customer)
