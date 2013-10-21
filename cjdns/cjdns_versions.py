#!/usr/bin/env python
import sys, os
try:
    from cjdnsadmin import connectWithAdminInfo
except ImportError:
    sys.path.append("/opt/cjdns/contrib/python/cjdnsadmin")
    from cjdnsadmin import connectWithAdminInfo
cjdns = connectWithAdminInfo()
timeout = 1000
if os.getenv("TIMEOUT") is not None:
	timeout = os.getenv("TIMEOUT")

def getVersions():
    more = True
    i = 0
    versions = {'error': 0, 'timeout': 0}
    nodes = []
    while more:
        table = cjdns.NodeStore_dumpTable(i)
        more = "more" in table
        for route in table['routingTable']:
            if not route['ip'] in nodes:
                nodes.append(route['ip'])
                print "Pinging %s..." % route['ip']
                if timeout is not None:
                    ping = cjdns.RouterModule_pingNode(route['ip'], timeout)
                else:
                    ping = cjdns.RouterModule_pingNode(route['ip'])
                if 'version' in ping:
                    if not ping['version'] in versions:
                        versions[ping['version']] = 0
                    versions[ping['version']] += 1
                elif 'result' in ping:
                    if ping['result'] == 'timeout':
                        #print "Timed out"
                        versions['timeout'] += 1
                elif 'error' in ping:
                    #print ping['error']
                    versions['error'] += 1
        i += 1
    return versions

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print """graph_title Cjdns Versions
graph_info This graph shows the which version of cjdns people are running
graph_category cjdns
graph_vlabel nodes
"""
    for version in getVersions().keys():
        print "%s.label %s" % (version, version)
        print "%s.draw AREASTACK" % version
else:
    versions = getVersions()
    for version in versions.keys():
        print "%s.value %s" % (version, versions[version])
