"""
# pip install influxdb-client
Uses InfluxDBClient to send metrics to an HTTP endpoint
This is a functional mode of sending the metrics to OTel Influx receiver

python3 influx_http_sender.py
"""

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

org_ = 'some-org-91'
bucket_ = 'bucket-92'

client = InfluxDBClient(url="http://localhost:19000", org=org_)
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket_, org_, ["h2o_feet_91,location=coyote_creek water_level=1"])
write_api.write(bucket_, org_, ["h2o_feet_92,location=coyote_creek water_level=1".encode()])
# Using a dict => explicitly specifying the pieces of the message
write_api.write(bucket_, org_, [{"measurement": "h2o_feet_93", "tags": {"location": "coyote_creek"}, "fields": {"water_level": 1}, "time": 1}])
