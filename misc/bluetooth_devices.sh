#!/bin/bash
if [ "$1" = "config" ]; then
    echo "graph_title Visible Bluetooth Devices"
    echo "graph_info This graph shows the number of bluetooth devices visible"
    echo "graph_category misc"
    echo "graph_vlabel devices"
    echo "devices.label devices"
    echo "devices.type GAUGE"
    echo "devices.draw LINE2"
    exit 0
fi

echo devices.value $(hcitool scan | grep -v "Scanning ..." | wc -l)
