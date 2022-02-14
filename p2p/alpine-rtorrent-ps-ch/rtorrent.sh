#!/bin/bash

#tc qdisc del dev eth0 root 2>/dev/null
#tc qdisc del dev eth0 ingress 2>/dev/null
#tc qdisc del dev ifb0 root 2>/dev/null

# ip link add ifb0 type ifb
# ip link set dev ifb0 up
# tc qdisc add dev eth0 ingress
# tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
#
# for dev in ifb0 eth0; do
#     tc qdisc replace dev $dev handle 10: root tbf rate 400mbit burst 1M latency 20ms peakrate 480mbit minburst 1529
# done

test -e ${DOWNLOADS}/.rtorrent/.session/rtorrent.lock && pidof rtorrent \
    || rm -f ${DOWNLOADS}/.rtorrent/.session/rtorrent.lock

/usr/bin/tmux -2u new -n rT-PS -s rtorrent -d \
    "ionice -c 3 nice -n 19 s6-setuidgid ${RTORRENT_USER} rtorrent"

tail -f /dev/null

