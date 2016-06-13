#!/usr/bin/env python
"""Creates a graph of IPFS's bandwidth usage."""
import requests
import os
import sys

api_base = os.getenv("IPFS_API", "http://localhost:5001/api/v0")

if "config" in sys.argv:
    print("""graph_title IPFS bandwidth
graph_info This graph shows the amount of bandwidth used by IPFS on this machine
graph_category ipfs
graph_order in out
graph_args --base 1000
graph_vlabel bits in (-) / out (+) per ${graph_period}
in.label received
in.type DERIVE
in.graph no
in.cdef in,8,*
in.min 0
out.label bps
out.type DERIVE
out.negative in
out.cdef out,8,*
out.min 0
out.max 100000000
out.info Traffic used by IPFS
in.max 100000000""")
else:
    data = requests.get("%s/stats/bw" % api_base).json()
    print("in.value %s" % data['TotalIn'])
    print("out.value %s" % data['TotalOut'])
