#!/usr/bin/env python
import requests
import json
import sys
import os

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
        
if config:
    print """graph_title Wireless Packets
graph_info This graph shows the volume of wireless packets
graph_category wireless

SWRXgoodPacket.label Packets Transmitted
SWRXgoodPacket.type DERIVE
SWRXgoodPacket.graph no
SWRXgoodPacket.min 0
SWTXgoodPacket.label Packets Received
SWTXgoodPacket.type DERIVE
SWTXgoodPacket.negative SWRXgoodPacket

SWTXerrorPacket.min 0
SWRXerrorPacket.label TX error
SWRXerrorPacket.type DERIVE
SWRXerrorPacket.graph no
SWRXerrorPacket.min 0
SWTXerrorPacket.label RX error
SWTXerrorPacket.type DERIVE
SWTXerrorPacket.negative SWRXerrorPacket
SWTXerrorPacket.min 0

graph_vlabel Packets"""
else:
    ip = "192.168.1.1"
    if os.getenv("HOST") is not None:
        if os.getenv("HOST") != "":
            ip = os.getenv("HOST")
    info = requests.get("http://" + ip + "/Info.live.htm").content.split("\n")
    
    for line in info:
        if "::" in line:
            key = line.split("::")[0].replace("{", "")
            data = line.split("::")[1].replace("}", "")
            
            if key == "packet_info":
                for line2 in data.split(";"):
                    if "=" in line2:
                        key2, value2 = line2.split("=")
                        print "%s.value %s" % (key2, value2)
