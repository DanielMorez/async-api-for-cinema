import os

from django.core.wsgi import get_wsgi_application

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware


sentry_sdk.init(
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = SentryWsgiMiddleware(get_wsgi_application())
