"""
Sample code that sends a metric in influx line protocol to a UDP socket

Equivalent using netcat:
echo "inf_tel_06,host=server-1,device=y79jx value=4.90" | nc -u localhost 8092

python3 influx_udp.py
"""
import random, string
import time
import socket


def randomword(length):
    # letters = string.ascii_lowercase
    letters = ['0', 'b', 'c']
    return ''.join(random.choice(letters) for i in range(length))


for idx in range(0, 10_000_000):
    # for idx in range(0, 10):
    message = f"a.b.c{randomword(16)}inf_tel_{randomword(6)},{randomword(5)}=server-{randomword(12)},{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx value={idx * 1000 / 7.0}"
    message = f"some_thing,Hostess=0ssa{randomword(12)},other=y{randomword(15)}jx,{randomword(4)}=yy{randomword(15)}jx value={idx * 1000 / 7.0}"
    print(message)
    time.sleep(1)
    # time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Sends influx metrics on UDP port 8092
    sock.sendto(message.encode(), ("localhost", 8092))
    sock.close()
