from __future__ import absolute_import
import os
from django.conf import settings 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minify.settings')

#app = Celery(broker=settings.CELERY_BROKER_URL)
app = Celery("minify")


app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

"""app.conf.update(
    CELERYBEAT_SCHEDULE={
        'rentplus_automation': {
            'task': 'vaultflex.rentplus_automation_task',
            'schedule': crontab(minute='*/1') 
        },
        'targetSavings_automation': {
            'task': 'vaultflex.targetSavings_automation_task',
            'schedule': crontab(minute='*/1')
        }
    }
)"""


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)