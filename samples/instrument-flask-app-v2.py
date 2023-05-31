"""
Manual instrumentation and periodic export to the Collector

# pip install opentelemetry-api
# pip install opentelemetry-sdk
# pip install opentelemetry-exporter-otlp-proto-http
# pip install opentelemetry-exporter-otlp-proto-grpc

Start the flask app
====================

Source: https://opentelemetry.io/docs/instrumentation/python/getting-started/

flask --app instrument-flask-app-v2.py run -p 8080

Service endpoint: http://localhost:8080/rolldice
"""

from random import randint
from flask import Flask

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
# For the grpc endpoint
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# For the HTTP endpoint
# from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

app = Flask(__name__)

# Other parameters:
# https://github.com/open-telemetry/opentelemetry-python/blob/main/exporter/opentelemetry-exporter-otlp-proto-grpc/src/opentelemetry/exporter/otlp/proto/grpc/metric_exporter/__init__.py#L79

# OTLPMetricExporter for GRPC endpoint
exporter = OTLPMetricExporter(
    endpoint='localhost:4317',
    # endpoint = 'http://localhost:4318/v1/metrics'#,
    insecure=True
)
# OTLPMetricExporter for GRPC endpoint
# For some reason, it requires the complete path to be specified
# exporter = OTLPMetricExporter(endpoint='http://localhost:4318/v1/metrics')

reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5_000,
    export_timeout_millis=5_000
)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

requests_hist = meter.create_histogram(
    name="requests_hgp",
    description="number of requests",
    unit="1"
)

requests_counter = meter.create_counter(
    name="foo_counter",
    description="Counts the number of Foos",
    unit="59"
)


@app.route("/rolldice")
def roll_dice():
    return str(do_roll())


def do_roll():
    res = randint(1, 1000)
    # requests_hist.record(1.0)
    requests_counter.add(res)
    return f'Random: {res}'
