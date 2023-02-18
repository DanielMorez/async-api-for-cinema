import logging

import logstash

from flask_jwt_extended import JWTManager
from flask import request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from config import settings
from utils.app_factory import create_app


sentry_sdk.init(
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


logging.basicConfig(level=logging.INFO)

logstash_handler = logstash.LogstashHandler(
    'logstash',
    settings.logstash_port,
    version=1,
    tags=['auth']
)


logging.getLogger().addFilter(RequestIdFilter())
logging.getLogger().addHandler(logstash_handler)

app = create_app(settings)
jwt = JWTManager(app)


if __name__ == "__main__":
    from config import settings

    app.run(host=settings.host, port=settings.port)
