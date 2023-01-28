from functools import wraps

from flask import Flask, request
from opentelemetry import trace as tr
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


def configure_tracer(host: str, port: int, service_name: str = "auth") -> None:
    resource = Resource(attributes={
        "service.name": service_name
    })
    tr.set_tracer_provider(TracerProvider(resource=resource))
    tr.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=host,
                agent_port=port,
            )
        )
    )
    tr.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


def init_jaeger(app: Flask):
    FlaskInstrumentor().instrument_app(app)


def trace():
    def wrapper(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            tracer = tr.get_tracer(request.path)
            with tracer.start_as_current_span(function.__name__) as span:
                span.set_attribute("args", args)
                span.set_attribute("kwargs", args)
            return function(*args, **kwargs)

        return decorator

    return wrapper
