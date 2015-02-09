#!/usr/bin/env python3
import requests
import sys
import os

nodes = os.getenv("fingerprints").split(" ")

request = requests.get("https://oniontip.com/result.json")
if isinstance(request.json, dict):
    results = request.json
else:
    results = request.json()

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print("""graph_title Oniontip Position
graph_info Shows the position in the oniontip list
graph_category tor
graph_vlabel Position
""")
    for node in results['results']:
        if node['fp'] in nodes:
            print("%s.label %s" % (node['fp'], node['nick']))
else:
    for node in results['results']:
        if node['fp'] in nodes:
            print("%s.value %s" % (node['fp'], node['index']))
