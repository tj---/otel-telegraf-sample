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

from opentelemetry.sdk.metrics.view import View, ExplicitBucketHistogramAggregation
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider, Histogram
# For the grpc endpoint
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# For the HTTP endpoint
# from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, AggregationTemporality

app = Flask(__name__)

# Other parameters:
# https://github.com/open-telemetry/opentelemetry-python/blob/main/exporter/opentelemetry-exporter-otlp-proto-grpc/src/opentelemetry/exporter/otlp/proto/grpc/metric_exporter/__init__.py#L79

# OTLPMetricExporter for GRPC endpoint
exporter = OTLPMetricExporter(
    endpoint='localhost:4317',
    # endpoint = 'http://localhost:4318/v1/metrics'#,
    insecure=True,
    preferred_temporality={Histogram: AggregationTemporality.CUMULATIVE}
)
# OTLPMetricExporter for GRPC endpoint
# For some reason, it requires the complete path to be specified
# exporter = OTLPMetricExporter(endpoint='http://localhost:4318/v1/metrics')

reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5_000,
    export_timeout_millis=5_000
)

hist_view_1 = View(
    instrument_type=Histogram,
    aggregation=ExplicitBucketHistogramAggregation(
        boundaries=(1, 20, 50, 100, 1000)
    )
)

provider = MeterProvider(metric_readers=[reader], views=[hist_view_1])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Instrumentation => Histogram
requests_histogram = meter.create_histogram(
    name="dice_roll_hist",
    description="Histogram for the dice roll requests"
)

# Instrumentation => Counter
requests_counter = meter.create_counter(
    name="dice_roll_counter",
    description="Counter for the dice roll requests",
    unit="59"
)


@app.route("/rolldice")
def roll_dice():
    return str(do_roll())


@app.route("/rolldice/<val>")
def fake_roll_dice(val):
    # requests_hist.record(int(val))
    return val


def do_roll():
    res = randint(0, 10_000)
    requests_histogram.record(res)
    requests_counter.add(res, attributes= {"app": "timescale"})
    return f'Random: {res}'
