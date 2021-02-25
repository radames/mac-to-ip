#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from time import sleep
import sys
import socket

if len(sys.argv) >= 2:
    mac = sys.argv[1]
    try:
        ip = sys.argv[2]
    except:
        ip = socket.gethostbyname(socket.gethostname()) #local ip
else:
    print("Insert MAC Address to search")
    sys.exit(0)

print(f'Here is your local ip {ip}')
nm = NmapProcess(f'{ip}/24', options="-sP")
nm.run_background()

while nm.is_running():
    print(f'Nmap Scan running: ETC: {nm.etc} DONE: {nm.progress}%')
    sleep(2)
nmap_report = NmapParser.parse(nm.stdout)

res = next(filter(lambda n:n.mac == mac.strip().upper(), filter(lambda host:host.is_up(), nmap_report.hosts)), None)
if res == None:
    print("Host is down or Mac address not exist")
else:
    print(f'\nMAC: {mac} with IP {res.address}')
