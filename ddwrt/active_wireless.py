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
    print """graph_title Wireless Clients
graph_info This graph shows the number of wireless clients on the DD-WRT router
graph_category wireless
active_wireless.label Clients
graph_vlabel Clients"""
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
            
            if key == "active_wireless":
                data = json.loads("[" + data.replace("'", "\"") + "]")
                
                print "active_wireless.value %i" % (len(data)/9)
