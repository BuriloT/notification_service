import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'notification_service.settings'
)

app = Celery('notification_service')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.enable_utc = False

app.conf.beat_schedule = {
    'run-every-thirty-seconds': {
        'task': 'api.tasks.send_mail',
        'schedule': 30.0
    }
}
