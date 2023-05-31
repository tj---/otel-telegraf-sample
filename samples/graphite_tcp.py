import socket
import time

"""
This sends the message to the Graphite receiver in OTel Collector

Equivalent using netcat:
"some_metric 100.5 1685012663" | nc localhost 2003
"""
# Create a socket
sock = socket.socket()

# For Telegraf input
# mode = "Diamond-Telegraf"
# sock.connect(('localhost', 2013))

# For OTel receiver
mode = "Diamond-OTel"
sock.connect(('localhost', 2003))

try:
    value = 100
    # Plain text format
    message = ""
    for idx in range(0, 50):
        time.sleep(1)
        value += 100
        message = "{} {} {}\n".format(f"Cluster.c891.node74.{mode}.temperature.max", value, int(time.time()))
        sock.send(message.encode())
        time.sleep(1)
        message = "{} {} {}\n".format(f"Cluster.c891.node74.{mode}.foo.bar.weather.xyz", value, int(time.time()))
        sock.send(message.encode())
finally:
    sock.close()
