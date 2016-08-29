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

nm = NmapProcess(ip+"/24",options="-sP")
nm.run_background()

while nm.is_running():
    print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nm.etc,nm.progress))
    sleep(2)
nmap_report = NmapParser.parse(nm.stdout)
res = list(filter(lambda n:n.mac == mac.strip().upper(), filter(lambda host:host.is_up(), nmap_report.hosts)))
if res ==[]:
    print("Host is down or Mac address not exist")
else:
    print("MAC: {} with IP {}".format(mac, res[0].address))
