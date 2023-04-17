import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if sentry_dsn := os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=sentry_dsn, integrations=[DjangoIntegration()], traces_sample_rate=1.0
    )
