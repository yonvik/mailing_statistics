# celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing_service.settings')

app = Celery('mailing_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'UTC'
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.autodiscover_tasks()
