"""
Sample code that sends a metric in influx line protocol to a UDP socket

Equivalent using netcat:
"inf_tel_06,host=server-1,device=y79jx value=4.90" | nc -u localhost 8092

python3 influx_udp.py
"""
import socket

message = "inf_tel_06,host=server-1,device=y79jx value=34.90"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Sends influx metrics on UDP port 8092
sock.sendto(message.encode(), ("localhost", 8092))
sock.close()
