#!/bin/bash

# throttle --up 300000 --down 360000 rtt:14

#tc qdisc del dev eth0 root 2>/dev/null
#tc qdisc del dev eth0 ingress 2>/dev/null
#tc qdisc del dev ifb0 root 2>/dev/null

ip link add ifb0 type ifb
ip link set dev ifb0 up
tc qdisc add dev eth0 ingress
tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0

for dev in ifb0 eth0; do
    tc qdisc replace dev $dev handle 10: root tbf rate 280mbit burst 512kb latency 5ms peakrate 300mbit minburst 1549
done

nice -n 19 ionice -c 3 s6-setuidgid ${RTORRENT_USER} rtorrent -n -o import=/config/rtorrent.rc-new -o system.daemon.set=true &

tail -f /dev/null


