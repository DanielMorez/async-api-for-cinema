import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-subscriptions": {
        "task": "billing.tasks.auto_payment",
        "schedule": 1 # crontab(minute=0, hour="*/1"),  # change to 1 times per a minute to test
    },
}

app.conf.timezone = "Europe/Moscow"
