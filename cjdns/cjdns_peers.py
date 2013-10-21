#!/usr/bin/env python
import sys
try:
    from cjdnsadmin import connectWithAdminInfo
except ImportError:
    sys.path.append("/opt/cjdns/contrib/python/cjdnsadmin")
    from cjdnsadmin import connectWithAdminInfo

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print """graph_title Cjdns Peers
graph_info This graph shows the number of peers cjdns is connected to.
graph_category cjdns
graph_vlabel peers
peers.label peers
peers.info Average number of peers for the last five minutes
peers.type GAUGE
peers.draw LINE2"""
else:
    cjdns = connectWithAdminInfo()
    print "peers.value %s" % cjdns.InterfaceController_peerStats()['total']
