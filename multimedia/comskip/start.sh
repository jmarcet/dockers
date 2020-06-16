#!/bin/sh

cleanuprecordings.sh | tee -a ${LOG_COMSKIP} &

comskip-recordings.py
