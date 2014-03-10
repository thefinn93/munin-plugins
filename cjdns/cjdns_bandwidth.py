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
        print "graph_title cjdns bandwidth"
        print "graph_vlabel bytes"
        print "graph_category cjdns"
        config = True

def name(peer):
    name = peer['publicKey']
    if "user" in peer:
        name = peer['user']
    if os.getenv("NAMES") != None and os.getenv("NAMES") != "":
        try:
            namefile = json.load(open(os.getenv("NAMES")))
        except IOError:
            sys.stderr.write("Error opening namefile " + os.getenv("NAMES") + "\n")
        except ValueError:
            sys.stderr.write("Error parsing namefile " + os.getenv("NAMES") + " - is it valid JSON?\n")
        else:
            if peer['publicKey'] in namefile:
                name = namefile[peer['publicKey']]
    return name

more = True
peers = []
page = 0

while more:
     data = cjdns.InterfaceController_peerStats(page)
     peers += data['peers']
     more = "more" in data
     page += 1

for peer in peers:
    if config:
        print peer['publicKey'][0:15] + "in.label " + name(peer)
        print peer['publicKey'][0:15] + "in.type DERIVE"
        print peer['publicKey'][0:15] + "in.graph no"
        print peer['publicKey'][0:15] + "in.min 0"
        print peer['publicKey'][0:15] + "out.label " + name(peer)
        print peer['publicKey'][0:15] + "out.type DERIVE"
        print peer['publicKey'][0:15] + "out.negative " + peer['publicKey'][0:15] + "in"
        print peer['publicKey'][0:15] + "out.min 0"

    else:
        print peer['publicKey'][0:15] + "in.value " + str(peer['bytesIn'])
        print peer['publicKey'][0:15] + "out.value " + str(peer['bytesOut'])
