"""
# pip install influxdb-client
Uses InfluxDBClient to send metrics to an HTTP endpoint
This is a functional mode of sending the metrics to OTel Influx receiver

python3 influx_http_sender.py
"""

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import random, string
import time

org_ = 'some-org-91'
bucket_ = 'bucket-92'

client = InfluxDBClient(url="http://localhost:19000", org=org_)
write_api = client.write_api(write_options=SYNCHRONOUS)


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


for idx in range(0, 1_000_000):
    write_api.write(bucket_, org_, ["h2o_feet_91,location=coyote_creek max=1"])
    write_api.write(bucket_, org_, ["h2o_feet_92,location=coyote_creek water_level=1".encode()])
    # Using a dict => explicitly specifying the pieces of the message
    measurement = f"h2o_feet_{idx % (1 + random.randint(0, 5000))}"
    id = idx % (1 + random.randint(0, 12000))
    r5 = randomword(5)
    data = [{"measurement": measurement, "tags":
        {"dataSource": f"[tagged_metrics_t_{id}]", "druid_metric": f"druid_jvm_druid_pool{id}", "hostname": f"ip-172-{r5}-39-44.ec2.internal", "service": "druid/middlemanager", "metric" :"druid_pool"},
                                     "fields": {"water_level": idx*1000/7.0}}]
    print(data)
    write_api.write(bucket_, org_, data)
    time.sleep(0.01)
