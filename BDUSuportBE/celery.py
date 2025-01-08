import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDUSuportBE.settings')

app = Celery("bdu_support")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = "bdu_support"
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    "sync_bdu_students": {
        "task": "bduSuport.tasks.cron_tasks.sync_bdu_students",
        "schedule": crontab(minute=0)
    }
}

