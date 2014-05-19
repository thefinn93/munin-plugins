#!/bin/bash
network=$(echo $0 | cut -d'_' -f3)
channel=$(echo $0 | cut -d'_' -f4)
if [ "$1" = "config" ]; then
    echo "graph_title $channel on $network"
    echo "graph_info This graph shows the amount of activity on $channel."
    echo "graph_category irc"
    echo "graph_vlabel lines"
    echo "lines.label lines"
    echo "lines.type COUNTER"
fi
export linecount=$(cat $HOME/.weechat/logs/irc.$network.*$channel.weechatlog | wc -l)
echo "lines.value $linecount"
