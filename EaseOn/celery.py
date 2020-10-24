from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EaseOn.settings')
app = Celery('EaseOn')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# app.conf.beat_schedule = {
#     'add-every-day-9pm': {
#         'task': 'organizations.tasks.send_daily_status_reports_for_all_centres',
#         'schedule': crontab(hour='15',
#                             minute=30,
#                             )
#     },
# }
