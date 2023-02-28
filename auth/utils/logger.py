import logging
import logstash
import sentry_sdk

from flask import request
from pydantic import AnyUrl
from sentry_sdk.integrations.flask import FlaskIntegration


logging.basicConfig(level=logging.INFO)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


def init_sentry(dsn: AnyUrl):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )


def init_logstash(dsn: AnyUrl):
    logstash_handler = logstash.LogstashHandler(
        dsn.host,
        int(dsn.port),
        version=1,
        tags=['auth']
    )

    logging.getLogger().addFilter(RequestIdFilter())
    logging.getLogger().addHandler(logstash_handler)
