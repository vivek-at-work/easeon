# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

# def startup():
#     from trackstats.models import Domain, Metric
#     Domain.objects.TICKTING = Domain.objects.register(
#         ref='tickting',
#         name='Ticketing')

#     Metric.objects.TICKETING_ORDER_COUNT  = Metric.objects.register(
#     domain=Domain.objects.TICKTING,
#     ref='ticket_count',
#     name='Number of tickets created')


class TicketsConfig(AppConfig):
    name = 'tickets'
    # def ready(self):
    #     import os
    #     if os.environ.get('RUN_MAIN'):
    #         startup()
