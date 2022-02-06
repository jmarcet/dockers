#!/bin/sh

[ -n "${PUID}" ] && _SUDO="s6-setuidgid ${PUID}"

# $_SUDO /app/cleanuprecordings.sh | $_SUDO tee -a ${LOG_COMSKIP} &

# $_SUDO /app/comskip-recordings.py

tail -f /dev/null
