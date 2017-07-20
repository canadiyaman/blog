# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os, logging
from celery import Celery

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')


class CeleryConfig(AppConfig):
    name = 'apps.taskapp'
    verbose_name = _('Celery Ayarları')

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)


def revoke(task_id):
    app.control.revoke(task_id)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request)) # pragma: no cover