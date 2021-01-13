from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# import django
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobipharma_project.settings')
# django.setup()
app = Celery('mobipharma_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace="CELERY")

# app.conf.beat_schedule ={
#     "after-15-seconds":{
#         'task':'notifications.tasks.send_email',
#         'schedule':15.0,
#         'args': ('emuswailit@gmail.com',)
#     }
# }

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))