#!/usr/bin/env python
import requests
import os,sys

try:
    subs = os.getenv("subs").split(",")
except:
    sys.exit(1)

config = False

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
        
if config:
    print "graph_title Subreddit subscriber count"
    print "graph_vlabel subscribers"
    print "graph_category reddit"

for sub in subs:
    if config:
        print sub + ".label Subscribers on /r/" + sub
    else:
        data = requests.get("http://www.reddit.com/r/" + sub + "/about.json")
        print sub + ".value " + str(data.json()['data']['subscribers'])

