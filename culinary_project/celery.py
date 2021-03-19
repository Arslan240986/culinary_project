import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culinary_project.settings')

app = Celery('culinary_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'send-spam-every-1-minute': {
#         'task': 'contact.tasks.send_success_subscribe',
#         'schedule': crontab(minute='*/1'),
#     },
# }

app.conf.timezone = 'UTC'