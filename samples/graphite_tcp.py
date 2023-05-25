import socket
import time

# Create a socket
sock = socket.socket()

# For Telegraf input
# mode = "Diamond-Telegraf"
# sock.connect(('localhost', 2013))

# For OTel receiver
mode = "Diamond-OTel"
sock.connect(('localhost', 2003))

try:
    value = 100.5
    # Plain text format
    message = ""
    for idx in range(0, 50):
        time.sleep(1)
        value += 100
        message = "{} {} {}\n".format(f"Cluster.c891.node74.{mode}.temperature.max", value, int(time.time()))
        sock.send(message.encode())
finally:
    sock.close()