import logging
from contextvars import ContextVar
from core.logstash import LogstashSettings

from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler


x_request_id: ContextVar[str] = ContextVar("x_request_id", default="")


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = x_request_id.get()
        return True


def init_logstash(logstash: LogstashSettings):
    logstash_handler = AsynchronousLogstashHandler(
        logstash.host,
        logstash.port,
        None,
        transport="logstash_async.transport.UdpTransport",
    )
    logstash_handler.formatter = LogstashFormatter(tags=["ugc"])
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().addHandler(logstash_handler)
    logging.getLogger().addFilter(RequestIdFilter())
