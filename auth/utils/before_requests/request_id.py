from flask import request
from opentelemetry import trace as tr


def before_request():
    request_id = request.headers.get("X-Request-Id")

    if not request_id:
        raise RuntimeError("request id is required")

    tracer = tr.get_tracer(request.path)
    with tracer.start_as_current_span("Getting X-Request-Id") as span:
        span.set_attribute("http.request_id", request_id)
