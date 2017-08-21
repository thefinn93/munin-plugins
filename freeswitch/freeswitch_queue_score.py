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

if len(sys.argv) == 1:
    for queue in queues['response']:
        data = {"arguments": "queue list members", "queue_name": queue['name']}
        members = apicall({"command": "callcenter_config", "data": data})
        time = 0
        for member in members['response']:
            time += int(member['score']) - int(member['base_score'])
        time = time/len(members['response']) if len(members['response']) > 0 else 0
        print('{}.value {}'.format(name(queue['name']), time))
elif sys.argv[1] == "config":
    print('graph_title Average Wait Time')
    print('graph_category freeswitch')
    print('graph_vlabel seconds')
    for queue in queues['response']:
        print('{}.label Average wait time'.format(name(queue['name'])))
elif sys.argv[1] == "autoconfig":
    print('yes')
