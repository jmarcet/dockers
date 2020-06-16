#!/bin/sh

SAVEIFS=$IFS
IFS=$( echo -en "\b\n")

inotifywait -m -r -e delete --format %w%f ${RECORDINGS} 2>/dev/null | while read LINE; do
	echo $LINE | grep -q '\.mpeg$' || continue
	dir=$( dirname $LINE )
	name=$( basename ${LINE/.mpeg} )
	echo "`date` '$LINE' has been deleted in '$dir'"
	find $dir/ -type f -name "${name}*" -delete
	if [ -d "$dir" -a "$dir" != "${RECORDINGS}" ]; then
		[ -n "$( find $dir/ -type f -name '*.mpeg' )" ] && \
			echo "`date` '$dir' is not empty" && \
			continue
		echo -n "`date` "; rm -frv $dir
		parent=$( dirname $dir )
		if [ -d "$parent" -a "$parent" != "${RECORDINGS}" ]; then
			[ -z "$( find $parent/ -type f -name '*.mpeg' )" ] && \
			echo -n "`date` " && rm -frv $parent || \
			echo "`date` '$parent' is not empty"
		fi
	fi
done

IFS=$SAVEIFS
