import socket
import time

"""
This sends the message to a Graphite receiver on TCP

OTel Collector: Port 2003 (Receiver)
Telegraf: Port 2013 (Input)

Equivalent using netcat:
echo "some_metric 100.5 1685012663" | nc localhost 2003
"""

configs = {
    'telegraf': {
        'mode': 'diamond-telegraf',
        'port': 2013
    },
    'otel': {
        'mode': 'diamond-otel',
        'port': 2003
    }
}


def generate_graphite_metrics(config_key):
    mode = configs[config_key]['mode']
    port = configs[config_key]['port']

    try:
        sock = socket.socket()
        sock.connect(('localhost', port))
        metrics = [
            f"Cluster.c891.node74.{mode}.temperature.max",
            f"Cluster.c891.node75.{mode}.foo.bar.weather.xyz",
            f"Cluster.lambda.gamma.{mode}.theta.alpha"
        ]
        value = 100
        for idx in range(0, 50000):
            time.sleep(1)
            value += 100
            for metric in metrics:
                message = "{} {} {}\n".format(metric, value, int(time.time()))
                sock.send(message.encode())
                time.sleep(1)
    finally:
        sock.close()


if __name__ == "__main__":
    generate_graphite_metrics('telegraf')
