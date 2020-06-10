#!/bin/sh

macchanger -m ${MAC_MOVISTAR2} eth1
/etc/init.d/bird start

start-stop-daemon --start --quiet --name Kodi-MovistarTV --chdir /home/MovistarTV.Server \
	--chuid nobody:nogroup --exec /opt/server.sh -u nobody -g nogroup \
	--nicelevel -15 --iosched real-time:0
