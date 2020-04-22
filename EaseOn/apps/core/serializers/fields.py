# -*- coding: utf-8 -*-
import pytz
from rest_framework import fields


class DateTimeField(fields.DateTimeField):
    """docstring for DateTimeField"""

    timezone = pytz.utc


class BooleanToTextField(fields.BooleanField):
    """docstring for DateTimeField"""

    def to_representation(self, value):
        if value in self.TRUE_VALUES:
            return 'yes'
        elif value in self.FALSE_VALUES:
            return 'no'
        if value in self.NULL_VALUES and self.allow_null:
            return None
        return bool(value)
