#!/usr/bin/env python3
import requests
import sys
import os

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print("""graph_title Oniontip Position
graph_info Shows the position in the oniontip list
graph_category tor
graph_vlabel Position
position.label Position
""")
else:
    request = requests.get("https://oniontip.com/result.json")
    if isinstance(request.json, dict):
        results = request.json
    else:
        results = request.json()
    fp = os.getenv("fp")
    index = None
    for node in results['results']:
        if node['fp'] == fp:
            index = node['index']
    print("position.value %s" % index)
