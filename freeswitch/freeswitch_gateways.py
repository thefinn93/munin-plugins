#!/usr/bin/env python3
import ESL
import sys
import re
import os

host = os.environ.get("FS_HOST", "127.0.0.1")
port = os.environ.get("FS_PORT", "8081")
password = os.environ.get("FS_PASSWORD", "ClueCon")

conn = ESL.ESLconnection(host, port, password)

name = sys.argv[0].split('/')[-1]

validname = re.compile('[\W_]+')


def parse_response(command):
    out = {}
    for line in conn.api(command).getBody().split('\n'):
        if '\t' in line:
            key, value = line.split('\t', 2)
            out[key.strip()] = value.strip()
    return out


gateways = []
for line in conn.api('sofia status gateway').getBody().split('\n'):
    if 'external::' in line:
        gateways.append(line.split('\t')[0].split('::')[-1])

for gateway in gateways:
    status = parse_response('sofia status gateway {}'.format(gateway))
    multigraph = "{}_{}".format(name, validname.sub('', gateway))
    for d in ["in", "out"]:
        if len(sys.argv) == 1:
            print("multigraph {}_{}".format(multigraph, d))
            print("calls_{}.value {}".format(d, status.get('Calls{}'.format(d.upper()))))
            print("failed_calls_{}.value {}".format(d, status.get('FailedCalls{}'.format(d.upper()))))
        elif sys.argv[1] == "config":
            print("multigraph {}_{}".format(multigraph, d))
            print('graph_title {} Calls {}'.format(gateway, d.title()))
            print('graph_vlabel calls')
            print('graph_category freeswitch')
            print('calls_{}.label Calls'.format(d))
            print('calls_{}.type DERIVE'.format(d))
            print('failed_calls_{}.label Failed Calls'.format(d))
            print('failed_calls_{}.type DERIVE'.format(d))
