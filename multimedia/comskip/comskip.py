#!/usr/bin/env python3

import logging as log
import os
import signal
import subprocess
import sys
import time
import timeit

from datetime import timedelta
from glob import glob

CHP_EXT = ".mkvtoolnix.chapters"
COMSKIP_INI = "/app/comskip.ini"
RECORDINGS = os.getenv("RECORDINGS")
TMP_EXT = ".tmp"
VID_EXT = ".mkv"

_nice = ("nice", "-n", "15", "ionice", "-c", "3")


def handle_cleanup(signum, frame):
    subprocess.run(["pkill", "comskip"])
    raise KeyboardInterrupt


def main():
    global proc

    log.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] [COMSKIP] [%(levelname)s] %(message)s",
        handlers=[log.FileHandler(os.path.join(RECORDINGS, "comskip.log")), log.StreamHandler(sys.stdout)],
        level=log.INFO,
    )

    files = [file for file in glob(f"{RECORDINGS}/**/*{CHP_EXT}", recursive=True)]
    files.sort(key=os.path.getmtime, reverse=True)
    for chapters in files:
        log.info(f'Processing "{chapters}"')

        _filename = os.path.splitext(os.path.splitext(chapters)[0])[0]
        command = list(_nice)
        command += ["mkvmerge", "-o", _filename + TMP_EXT]
        command += ["--chapters", chapters, _filename + VID_EXT]
        proc = subprocess.run(command)
        if proc.returncode:
            log.error(f'Could not parse "{chapters}"')
            os.remove(chapters)
            continue
        oldtime = os.path.getmtime(_filename + VID_EXT)
        os.rename(_filename + TMP_EXT, _filename + VID_EXT)
        os.utime(_filename + VID_EXT, (-1, oldtime))
        os.remove(chapters)

    now = time.time()
    files = [
        file
        for file in glob(f"{RECORDINGS}/**/*{VID_EXT}", recursive=True)
        if (
            not os.path.exists(os.path.splitext(file)[0] + ".edl")
            or os.path.getmtime(os.path.splitext(file)[0] + ".edl") < os.path.getmtime(file)
        )
        and (now - os.path.getmtime(file)) > 1200
    ]
    files.sort(key=os.path.getmtime, reverse=True)

    [signal.signal(sig, handle_cleanup) for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)]

    for recording in files:
        log.info(f'Processing "{recording}"')

        command = list(_nice)
        command += ["comskip", f"--ini={COMSKIP_INI}", "--hwassist", "-d", "70", recording]
        _start = timeit.default_timer()
        proc = subprocess.run(command)
        _end = timeit.default_timer()
        msg = f'"{recording}": {str(timedelta(seconds=(_end - _start)))} [{proc.returncode}]'
        _filename = os.path.splitext(recording)[0]
        if proc.returncode:
            log.warning(msg)
            os.remove(_filename + CHP_EXT)
            continue
        command = list(_nice)
        command += ["mkvmerge", "-o", _filename + TMP_EXT]
        command += ["--chapters", _filename + CHP_EXT, recording]
        proc = subprocess.run(command)
        if proc.returncode:
            log.warning(msg)
            raise ValueError(proc.returncode)
        oldtime = os.path.getmtime(recording)
        os.rename(_filename + TMP_EXT, recording)
        os.utime(recording, (-1, oldtime))
        os.remove(_filename + CHP_EXT)


try:
    main()
except (KeyboardInterrupt, ValueError):
    pass
finally:
    log.info("Good bye!")
