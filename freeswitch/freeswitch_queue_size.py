#!/usr/bin/env python3
import ESL
import sys
import json
import re
import os

host = os.environ.get("FS_HOST", "127.0.0.1")
port = os.environ.get("FS_PORT", "8081")
password = os.environ.get("FS_PASSWORD", "ClueCon")

conn = ESL.ESLconnection(host, port, password)
validname = re.compile('[\W_]+')


def apicall(command):
    apicmd = 'json {}'.format(json.dumps(command))
    result = conn.api(apicmd).getBody()
    return json.loads(result)


def name(name):
    return validname.sub('', name)


queues = apicall({"command": "callcenter_config", "data": {"arguments": "queue list"}})
states = ["Unknown", "Waiting", "Trying", "Answered", "Abandoned"]

for q in queues['response']:
    queue = q['name']
    print('multigraph freeswitch_queue_size_{}'.format(name(queue)))
    if len(sys.argv) == 1:
        data = {"arguments": "queue list members", "queue_name": queue}
        members = apicall({"command": "callcenter_config", "data": data})
        sizes = dict([(x, 0) for x in states])
        for member in members['response']:
            sizes[member['state']] += 1
        for state in sizes:
            print('{}.value {}'.format(name(state), sizes[state]))
    elif sys.argv[1] == "config":
        print('graph_title Queue {} Size'.format(queue))
        print('graph_category freeswitch')
        for state in states:
            print('{}.draw {}'.format(state, 'AREA' if states[0] == state else 'STACK'))
            print('{}.min 0'.format(state))
            print('{}.label {}'.format(state, state))
