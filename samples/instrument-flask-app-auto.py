"""
# pip install flask
# pip install opentelemetry-distro
# pip install opentelemetry-exporter-otlp

OpenTelemetry supports Auto-Instrumentation: https://opentelemetry.io/docs/instrumentation/python/automatic/
"Automatic instrumentation makes use of a Python agent that dynamically injects bytecode to capture telemetry from many popular libraries and frameworks."

Instrumentation libraries corresponding to popular frameworks can be installed by `opentelemetry-bootstrap`
# Instrument only a specific library
# pip install opentelemetry-instrumentation-flask==0.39b0

Additional instrumentation (manual) can be done in tandem

Start the flask app
====================

Source: https://opentelemetry.io/docs/instrumentation/python/getting-started/

opentelemetry-instrument \
    --traces_exporter none \
    --service_name foo-inst-service \
    flask --app instrument-flask-app-auto.py run -p 8080

Service endpoint: http://localhost:8080/rolldice
"""

from random import randint
from flask import Flask

# Also including manual instrumentation
from opentelemetry import metrics

# Acquire a meter.
meter = metrics.get_meter("diceroller.meter")

# Now create a counter instrument to make measurements with
roll_counter = meter.create_counter(
    "rolls_counter",
    description="The number of rolls by roll value",
)

app = Flask(__name__)


@app.route("/rolldice")
def roll_dice():
    return str(do_roll())


def do_roll():
    res = randint(1, 1000)
    roll_counter.add(1, {"roll.value": res})
    return res
