#!/usr/bin/env python

import os
import sys
import json

try:
    from cjdnsadmin import connect,connectWithAdminInfo
except ImportError:
    sys.path.append(os.getenv("cjdnsadmin","/opt/cjdns/contrib/python/cjdnsadmin"))
    from cjdnsadmin import connect,connectWithAdminInfo
    
if os.getenv("cjdns_password") is not None:
    cjdns = connect(os.getenv("cjdns_ip", "127.0.0.1"), int(os.getenv("cjdns_port", "11234")), os.getenv("cjdns_password"))
else:
    cjdns = connectWithAdminInfo()

try:
    cjdns.InterfaceController_peerStats()
except AttributeError:
    print "InterfaceController_peerStats() not a function"
    print "Do you have an old version of cjdns?"
    print "possibly the stable-0.4 branch."
    sys.exit(1)

config = False

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        print "graph_title Hyperboria known nodes"
#        print "graph_vlabel nodes"
        print "graph_category cjdns"
        print "nodes.label nodes"
        config = True


more = True
i = 0
routes = 0
nodes = []


while more and not config:
    table = cjdns.NodeStore_dumpTable(i)
    more = "more" in table
    routes += len(table['routingTable'])
    for route in table['routingTable']:
        if not route['ip'] in nodes:
            nodes.append(route['ip'])
    i += 1

if not config:
    print "nodes.value " + str(len(nodes))
