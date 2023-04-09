import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-subscriptions": {
        "task": "billing.tasks.auto_payment",
        "schedule": 1,  # change to 3 times per a day
    },
}

app.conf.timezone = "Europe/Moscow"
