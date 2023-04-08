import os

CELERY_BROKER_URL = os.environ.get("REDIS_DSN")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_DSN")
