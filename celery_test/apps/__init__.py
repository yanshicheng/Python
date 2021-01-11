

from celery import Celery

app = Celery('test_task')

app.config_from_object('apps.celery_conf')