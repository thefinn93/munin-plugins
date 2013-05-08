#!/bin/bash

if [ "$1" = "config" ]; then
    echo "graph_title Cjdns Peers"
    echo "graph_info This graph shows the number of peers cjdns is connected to."
    echo "graph_category network"
    echo "peers.label peers"
fi

if [ -z $CJDCMD ]; then
    CJDCMD=`which cjdcmd`
fi

args="-nodns"

## CJDCMD doesn't seem to actually support this, despite what the README sez
## Follow this at https://github.com/inhies/cjdcmd/issues/36

if [ "$pass" != "" ]; then
    args="$args --pass=\"$pass\"";
fi

if [ "$host" != "" ]; then
    args="$args --host=${host}"
fi

if [ "$port" != "" ]; then
    args="$args --port=${port}"
fi

echo "peers.value `$CJDCMD peers $args | wc -l`"
