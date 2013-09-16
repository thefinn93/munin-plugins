#!/usr/bin/env python
import sys
impot os
 
config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
 
if config:
    print """graph_title Reddit Karma
graph_info This graph shows the amount of karma that """ + os.getenv("username") + """ has.
graph_category misc
link.label Link Karma
comment.label Comment Karma"""
else:
    import requests
    import json
 
    domain = os.getenv("domain")
    if domain == "":
        domain = "www.reddit.com"
    user = os.getenv("username")
 
    about = json.loads(requests.get("http://" + domain + "/user/" + user + "/about.json"
    print "link.value " + str(about['data']['link_karma'])
    print "comment.value " + str(about['data']['comment_karma'])
