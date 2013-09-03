#!/usr/bin/env python

import os
import sys
import json

sys.path.append("/opt/cjdns/contrib/python/cjdnsadmin")

try:
    import cjdnsadmin
except ImportError:
    print "Could not find cjdnsadmin in: "
    for dir in sys.path:
        print dir
    sys.exit(1)

cjdns = cjdnsadmin.connectWithAdminInfo()

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
        print "graph_category network"
        config = True

def name(peer):
    name = peer['pubkey']
    if os.getenv("NAMES") != None and os.getenv("NAMES") != "":
        try:
            namefile = json.load(open(os.getenv("NAMES")))
        except IOError:
            sys.stderr.write("Error opening namefile " + os.getenv("NAMES") + "\n")
        except ValueError:
            sys.stderr.write("Error parsing namefile " + os.getenv("NAMES") + " - is it valid JSON?\n")
        else:
            if pubkey in namefile:
                name = namefile[peer['pubkey']]
            elif "user" in peer:
                name = peer['user']
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
        print peer['publicKey'].replace(".k", "") + "in.label " + name(peer)
        print peer['publicKey'].replace(".k", "") + "in.type DERIVE"
        print peer['publicKey'].replace(".k", "") + "in.graph no"
        print peer['publicKey'].replace(".k", "") + "in.min 0"
        print peer['publicKey'].replace(".k", "") + "out.label " + name(peer)
        print peer['publicKey'].replace(".k", "") + "out.type DERIVE"
        print peer['publicKey'].replace(".k", "") + "out.negative " + peer['publicKey'].replace(".k", "") + "in"
        print peer['publicKey'].replace(".k", "") + "out.min 0"

    else:
        print peer['publicKey'].replace(".k", "") + "in.value " + str(peer['bytesIn'])
        print peer['publicKey'].replace(".k", "") + "out.value " + str(peer['bytesOut'])
