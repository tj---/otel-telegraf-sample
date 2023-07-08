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

def rn(start, end):
    return random.randint(start, end)

m_sum = 0
count = 0
for idx in range(0, 10_000_000):
    # for idx in range(0, 10):
    message = f"a.b.c{randomword(16)}inf_tel_{randomword(6)},{randomword(5)}=server-{randomword(12)},{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx,{randomword(4)}=y{randomword(15)}jx value={idx * 1000 / 7.0}"
    message = f"some_thing,Hostess=0ssa{randomword(12)},other=y{randomword(15)}jx,{randomword(4)}=yy{randomword(15)}jx value={idx * 1000 / 7.0}"
    message = f"static_metric,Hostess=x0host-1,other=foo value={5}"
    rn1 = rn(1, 5)
    rn2 = rn(1, 20)
    rn3 = rn(1, 30)
    rn4 = rn(1, 5)
    count = count + 4
    m_sum = m_sum + (rn1 + rn2 + rn3 + rn4)

    # message = f"try_histo,Host=x0host-1,other=foo bucket_5={rn1},bucket_10={rn2},bucket_15={rn3},bucket_20={rn4},count={count},sum={sum}"
    # This gets translated to histogram directly
    message = f"try_histo_3,Host=x0host-1,other=foo 5={rn1},10={rn2},15={rn3},20={rn4},count={count},sum={m_sum},p_97=100"
    # Quantile test
    message = f"try_q_1,Host=x0host-1,other=foo try_q_count={rn1},try_q_1m_count={rn2},try_q_1m_p25={rn3},try_q_1m_min={rn4}"
    print(message)
    time.sleep(1)
    # time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Sends influx metrics on UDP port 8092
    sock.sendto(message.encode(), ("localhost", 8092))
    sock.close()
