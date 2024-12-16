import os
from celery import Celery

# celery -A BDUSuportBE worker -l info --autoscale 3,10

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDUSuportBE.settings')

app = Celery("bdu_support")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = "bdu_support"
app.conf.broker_connection_retry_on_startup = True

