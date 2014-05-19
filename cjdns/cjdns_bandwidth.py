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
        config = True

def name(peer):
    name = peer['publicKey'][0:10]
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
peers = {}
page = 0

while more:
     data = cjdns.InterfaceController_peerStats(page)
     for peer in data['peers']:
       peername = name(peer)
       if not peername in peers:
         peers[peername] = []
       peers[peername].append(peer)
     more = "more" in data
     page += 1

#print json.dumps(peers, sort_keys=True, indent=4, separators=(',', ': '))

for peer in peers:
    print "multigraph cjdns_%s" % peer
    if config:
        print "graph_title cjdns bandwidth for %s" % peer
        print "graph_vlabel bits"
        print "graph_category cjdns"
        for node in peers[peer]:
          print "in_%s.label %s" % (node['publicKey'][0:10], node['publicKey'])
          print "in_%s.type DERIVE" % node['publicKey'][0:10]
          print "in_%s.graph no" % node['publicKey'][0:10]
          print "in_%s.draw STACK" % node['publicKey'][0:10]
          print "in_%s.min 0" % node['publicKey'][0:10]
          print "out_%s.label %s" % (node['publicKey'][0:10], node['publicKey'])
          print "out_%s.type DERIVE" % node['publicKey'][0:10]
          print "out_%s.draw STACK" % node['publicKey'][0:10]
          print "out_%s.negative in" % node['publicKey'][0:10]
          print "out_%s.min 0\n" % node['publicKey'][0:10]

    else:
        for node in peers[peer]:
            print "in_%s.value %s" % (node['publicKey'][0:10], str(node['bytesIn']))
            print "out_%s.value %s\n" % (node['publicKey'][0:10], str(node['bytesOut']))
