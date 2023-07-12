"""
pip install signalfx

python3 sfx_app.py
"""
import signalfx
import time


def publish_sfx_metrics():
    sfx = signalfx.SignalFx(api_endpoint='http://127.0.0.1:9943',
                            ingest_endpoint='http://127.0.0.1:9943',
                            stream_endpoint='http://127.0.0.1:9943')

    ingest = sfx.ingest('ORG_TOKEN')

    for idx in range(0, 50000):
        time.sleep(2)
        ingest.send(
            gauges=[
                {
                    'metric': 'sfx.foo.bar.gamma',
                    'value': 100 + idx,
                    'timestamp': round(time.time() * 1000),
                    'dimensions': {'host': 'server-3810', 'host_ip': '11.2.3.44', 'source': 'sfx-client'}
                },
            ])

    sfx.stop()


if __name__ == "__main__":
    publish_sfx_metrics()
