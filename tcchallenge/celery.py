import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcchallenge.settings')

app = Celery('tcchallenge')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task(bind=True)
def hello_world(self):
    print('Hello world!')
