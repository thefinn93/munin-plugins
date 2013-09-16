#!/usr/bin/env python
import sys
import os

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True

if config:
    print """graph_title Clear Bars
graph_info This graph shows the number or bars on the clear modem.
graph_category wireless
bars.label Bars
bars.draw AREASTACK
bars.color 00FF00
graph_vlabel Bars"""
else:
    import requests
    modem = "192.168.15.1"
    if os.getenv("MODEM") != "" and os.getenv("MODEM") != None:
        modem = os.getenv("MODEM")
    status = requests.get("http://" + modem + "/cgi-bin/webcm?getpage=/usr/www/wimax_status.html").content.strip().split(":")
    bars = status[3]
    if bars == "":
        bars = "0"
    print "bars.value " + bars
