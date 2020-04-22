# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.admin import register
from slas.models import SLA, Term

register(SLA)
register(Term)
