#!/bin/sh

export HOME="/home"
export PATH="/opt/MovistarTV.Server:$PATH"

hash -r

LOG=log/log.txt

while true; do
	echo "MovistarTV Server starting" | tee -a $LOG
	Kodi-MovistarTV
	echo "MovistarTV Server died" | tee -a $LOG
	RECENT=$( find Timers/ -type f -mtime -1 | sed -e 's:Timers/::g' -e 's:\.xml::g' )
	for file in $RECENT; do rm -fr `find . -iname "*${file}*"`; done
	sync
done
