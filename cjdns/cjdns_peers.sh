#!/bin/bash

if [ "$1" = "config" ]; then
    echo "graph_title Cjdns Peers"
    echo "graph_info This graph shows the number of peers cjdns is connected to."
    echo "graph_category cjdns"
    echo "graph_vlabel peers"
    echo "peers.label peers"
    echo "peers.info Average number of peers for the last five minutes"
    echo "peers.type GAUGE"
    echo "peers.draw LINE2"
    exit 0
fi

if [ -z $CJDCMD ]; then
    CJDCMD=`which cjdcmd`
fi

args="-nodns"

if [ "$file" != "" ]; then
    args="$args -file=${file}"
fi

echo "peers.value `$CJDCMD peers $args | wc -l`"
