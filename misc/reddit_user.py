#!/usr/bin/env python
import sys
import os
 
config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True

user = os.getenv("username", "waaghals")

if config:
    print "graph_title Reddit Karma"
    print "graph_info This graph shows the amount of karma that " + user + " has."
    print "graph_category misc"
    print "link.label Link Karma"
    print "comment.label Comment Karma"
else:
    import requests
    import json
 
    domain = os.getenv("domain", "www.reddit.com")

    url = "http://" + domain + "/user/" + user + "/about.json"
    response = requests.get(url).content
    about = json.loads(response)
    
    print "link.value " + str(about['data']['link_karma'])
    print "comment.value " + str(about['data']['comment_karma'])
