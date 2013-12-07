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
    print "peers.value %s" % cjdns.InterfaceController_peerStats()['total']
