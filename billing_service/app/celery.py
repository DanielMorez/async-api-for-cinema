import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {}
app.conf.timezone = "Europe/Moscow"


@app.task
def auto_payments():
    # TODO: find subscriptions and create a payment
    pass
