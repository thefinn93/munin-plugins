#!/usr/bin/env python
import sys,os
try:
    from cjdnsadmin import connect,connectWithAdminInfo
except ImportError:
    sys.path.append(os.getenv("cjdnsadmin","/opt/cjdns/contrib/python/cjdnsadmin"))
    from cjdnsadmin import connect,connectWithAdminInfo

if os.getenv("cjdns_password") is not None:
    cjdns = connect(os.getenv("cjdns_ip", "127.0.0.1"), int(os.getenv("cjdns_port", "11234")), os.getenv("cjdns_password"))
else:
    cjdns = connectWithAdminInfo()

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True

allPeers = {}

i = 0
while True:
    ps = cjdns.InterfaceController_peerStats(i);
    peers = ps['peers']
    for p in peers:
        if p['state'] != 'ESTABLISHED':
            continue
        name = p['publicKey'][-10:]
        if "user" in p:
            name = p['user']
        if not name in allPeers:
            allPeers[name] = 0
        allPeers[name] =+ 1
    if (not 'more' in ps):
        break
    i += 1
if config:
    print "graph_title Cjdns Peers"
    print "graph_info This graph shows the number of peers cjdns is connected to."
    print "graph_category cjdns"
    print "graph_vlabel Connected Nodes"
    for peer in allPeers:
        print "%s.label %s" % (peer.replace(" ", "-"), peer)
        print "%s.draw AREASTACK" % peer.replace(" ", "-")
    print "total.label total"
    print "total.type GAUGE"
    print "total.draw LINE2"
else:
    for peer in allPeers:
        print "%s.value %s" % (peer.replace(" ", "-"), allPeers[peer])
    print "total.value %s" % cjdns.InterfaceController_peerStats()['total']
