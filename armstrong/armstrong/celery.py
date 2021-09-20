import os

from celery import Celery

app = Celery('armstrong')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
import payment.tasks


@app.task(bind=True)
def debug_task(self):
        print(f'Request: {self.request!r}')
