# -*- coding: utf-8 -*-
import django_filters


class FullNameFilter(django_filters.CharFilter):
    empty_value = 'EMPTY'

    def filter(self, qs, value):
        if value:
            first_name = value.split()[0]
            f_name='first_name'
            if self.field_name!='full_name':
                f_name = self.field_name + '__first_name'
            d = {f_name: first_name}
            qs = qs.filter(**d)
            if len(value.split()) > 1:
                last_name = value.split()[1]
                l_name='last_name'
                if self.field_name !='full_name':
                    l_name = self.field_name + '__last_name'
                d = {l_name: last_name}
                qs = qs.filter(**d)
        return qs
