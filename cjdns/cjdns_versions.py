#!/usr/bin/env python
import sys
import os
try:
    from cjdnsadmin import connect, connectWithAdminInfo
except ImportError:
    sys.path.append(os.getenv("cjdnsadmin",
                              "/opt/cjdns/contrib/python/cjdnsadmin"))
    from cjdnsadmin import connect, connectWithAdminInfo

if os.getenv("cjdns_password") is not None:
    cjdns = connect(os.getenv("cjdns_ip", "127.0.0.1"),
                    int(os.getenv("cjdns_port", "11234")),
                    os.getenv("cjdns_password"))
else:
    cjdns = connectWithAdminInfo()

timeout = int(os.getenv("TIMEOUT", "1000"))


def getVersions():
    more = True
    i = 0
    versionData = {}
    nodes = []
    highestversion = 0
    lowestversion = 2
    while more:
        table = cjdns.NodeStore_dumpTable(i)
        more = "more" in table
        for route in table['routingTable']:
            if not route['ip'] in nodes:
                if not route['version'] in versionData:
                    versionData[route['version']] = 0
                    if route['version'] > highestversion:
                        highestversion = route['version']
                versionData[route['version']] += 1
        i += 1
    for v in range(lowestversion, highestversion):
        if not v in versionData:
            versionData[v] = 0
    return versionData

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print """graph_title Cjdns Versions
graph_info This graph shows the which version of cjdns people are running
graph_category cjdns
graph_vlabel nodes
print "graph_args --upper-limit 130
"""
    for version in getVersions().keys():
        print "v%s.label v%s" % (version, version)
        print "v%s.draw AREASTACK" % version
else:
    versions = getVersions()
    for version in versions.keys():
        print "v%s.value %s" % (version, versions[version])
