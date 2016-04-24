from __future__ import absolute_import

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

from celery import Celery
from django.conf import settings


app = Celery('django_project')
app.config_from_object('django.conf:settings')

# load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
