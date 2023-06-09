A small setup for trying out [**OpenTelemetry Collector**](https://opentelemetry.io/docs/collector/) capabilities in tandem with [**Telegraf**](https://www.influxdata.com/time-series-platform/telegraf/) for `metrics`.

### Metric Formats 
- Influx
- Graphite (Carbon)
- OpenTelemetry

### Remote Backend
- Prometheus

### Samples
- [influx_udp.py](samples/influx_udp.py): Sample for sending a metric in influx line protocol to a UDP socket
- [influx_http_sender.py](samples/influx_http_sender.py): Sample for sending influx metrics using InfluxDBClient
- [graphite_tcp.py](samples/graphite_tcp.py): Sample for sending graphite metrics over tcp
- [instrument-flask-app-auto.py](samples/instrument-flask-app-auto.py): OTel (auto & manual) instrumentation of a Flask app 
- [instrument-flask-app-v2.py](samples/instrument-flask-app-v2.py): OTel instrumentation  of a Flask app and periodic export

### Setup
- [**Docker**](docker_compose.yml) containers: `Telegraf`, `Prometheus`, `otel-collector`
- [**Prometheus**](prometheus.yml) config: Scraping from OTel (exporter) and Telegraf (Output plugin)
- [**OTel Collector**](otel-collector-config.yaml) config: Metrics pipeline:  `receivers: [influxdb, otlp, graphite]` and `exporters: [file/file-A, file/file-B, logging, prometheus]`
- [**Telegraf**](telegraf.conf) config: `Inputs: influx, graphite` and `Outputs: influxdb_v2, opentelemetry, file, prometheus_client`
- [**Graphite Exporter**](graphite_mapping.conf) config: In: Graphite => Out: Prom (Scraping)

### Start
```shell
# In the root directory
docker-compose -f docker_compose.yml up -d
# Run the samples. Eg: 
flask --app instrument-flask-app-v2.py run -p 8080
# Observer the Prometheus Metrics:
http://localhost:9090/graph
```
