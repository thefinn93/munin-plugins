#!/usr/bin/env python
import ESL
import sys
import json
import os

host = os.environ.get("FS_HOST", "127.0.0.1")
port = os.environ.get("FS_PORT", "8081")
password = os.environ.get("FS_PASSWORD", "ClueCon")

conn = ESL.ESLconnection(host, port, password)

if len(sys.argv) == 1:
    channels = json.loads(conn.api('show channels as json').getBody())
    print('channels.value {}'.format(channels.get('row_count')))
elif sys.argv[1] == "config":
    print('graph_title Channels Used')
    print('graph_vlabel channels')
    print('graph_category freeswitch')
    print('channels.label channels')
elif sys.argv[1] == "autoconfig":
    print('yes')
