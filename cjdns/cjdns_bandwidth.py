#!/usr/bin/env python

import os
import sys
import json
import re
from hashlib import sha512

try:
    from cjdnsadmin import connect,connectWithAdminInfo
except ImportError:
    sys.path.insert(0, os.getenv("cjdnsadmin","/opt/cjdns/contrib/python/cjdnsadmin"))
    from cjdnsadmin import connect,connectWithAdminInfo

if os.getenv("cjdns_password") is not None:
    cjdns = connect(os.getenv("cjdns_ip", "127.0.0.1"), int(os.getenv("cjdns_port", "11234")), os.getenv("cjdns_password", "NONE"))
else:
    cjdns = connectWithAdminInfo()

try:
    cjdns.InterfaceController_peerStats()
except AttributeError:
    print "InterfaceController_peerStats() not a function"
    print "Do you have an old version of cjdns?"
    print "possibly the stable-0.4 branch."
    sys.exit(1)

## Stolen from contrib/python/cjdnsadmin/publicToIp6.py ##

# see util/Base32.h
def Base32_decode(input):
    output = bytearray(len(input));
    numForAscii = [
        99,99,99,99,99,99,99,99,99,99,99,99,99,99,99, 99,
        99,99,99,99,99,99,99,99,99,99,99,99,99,99,99, 99,
        99,99,99,99,99,99,99,99,99,99,99,99,99,99,99, 99,
         0, 1, 2, 3, 4, 5, 6, 7, 8, 9,99,99,99,99,99, 99,
        99,99,10,11,12,99,13,14,15,99,16,17,18,19,20, 99,
        21,22,23,24,25,26,27,28,29,30,31,99,99,99,99, 99,
        99,99,10,11,12,99,13,14,15,99,16,17,18,19,20, 99,
        21,22,23,24,25,26,27,28,29,30,31,99,99,99,99, 99,
    ];

    outputIndex = 0;
    inputIndex = 0;
    nextByte = 0;
    bits = 0;

    while (inputIndex < len(input)):
        o = ord(input[inputIndex]);
        if (o & 0x80): raise ValueError;
        b = numForAscii[o];
        inputIndex += 1;
        if (b > 31): raise ValueError("bad character " + input[inputIndex]);

        nextByte |= (b << bits);
        bits += 5;

        if (bits >= 8):
            output[outputIndex] = nextByte & 0xff;
            outputIndex += 1;
            bits -= 8;
            nextByte >>= 8;

    if (bits >= 5 or nextByte):
        raise ValueError("bits is " + str(bits) + " and nextByte is " + str(nextByte));

    return buffer(output, 0, outputIndex);


def PublicToIp6_convert(pubKey):
    if (pubKey[-2:] != ".k"): raise ValueError("key does not end with .k");
    keyBytes = Base32_decode(pubKey[0:-2]);
    hashOne = sha512(keyBytes).digest();
    hashTwo = sha512(hashOne).hexdigest();
    first16 = hashTwo[0:32];
    out = '';
    for i in range(0,8): out += first16[i*4 : i*4+4] + ":";
    return out[:-1];


## /theft ##


config = False

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True

def name(peer):
    name = peer['publicKey'][0:9]
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
    print "multigraph cjdns_%s" % (re.sub(r'[^A-Za-z0-9_]', '_', peer))[0:20]
    if config:
        print "graph_title cjdns bandwidth for %s" % peer
        print "graph_vlabel Bytes in (+) and out (-)"
        print "graph_category cjdns"
        for node in peers[peer]:
          print "in_%s.label %s" % (node['publicKey'][0:10], PublicToIp6_convert(node['publicKey']))
          print "in_%s.type DERIVE" % node['publicKey'][0:10]
          print "in_%s.graph no" % node['publicKey'][0:10]
          print "in_%s.min 0" % node['publicKey'][0:10]
          print "out_%s.label %s" % (node['publicKey'][0:10], PublicToIp6_convert(node['publicKey']))
          print "out_%s.type DERIVE" % node['publicKey'][0:10]
          print "out_%s.negative in_%s" % (node['publicKey'][0:10], node['publicKey'][0:10])
          print "out_%s.min 0\n" % node['publicKey'][0:10]

    else:
        for node in peers[peer]:
            print "in_%s.value %s" % (node['publicKey'][0:10], str(node['bytesIn']))
            print "out_%s.value %s\n" % (node['publicKey'][0:10], str(node['bytesOut']))
