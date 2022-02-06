#!/usr/bin/env python3

import asyncio
import logging as log
import os

from glob import glob

COMSKIP_INI = "/app/comskip.ini"
RECORDINGS = os.getenv("RECORDINGS")
LOCK_COMSKIP = "/tmp/.comskip.lock"
LOCK_MKVMERGE = "/tmp/.mkvmerge.lock"
LOGFILE = os.path.join(RECORDINGS, "comskip.log")

CHP_EXT = ".mkvtoolnix.chapters"
MRG_EXT = ".mkv-merged"
TXT_EXT = ".txt"
VID_EXT = ".mkv"

_nice = ("nice", "-n", "15", "ionice", "-c", "3", "flock")


def cleanup(filename, _check=True):
    [
        os.remove(x)
        for x in glob(f"{filename}.*")
        if os.splitext(x)[1] not in (TXT_EXT, VID_EXT, ".jpg", ".nfo")
    ]
    if _check and (
        not os.path.exists(filename + TXT_EXT)
        or not os.path.getsize(filename + TXT_EXT)
    ):
        if os.path.exists(filename + VID_EXT):
            log.info(
                f"[WARNING]: something went wrong analyzing {filename}{VID_EXT}, marking as already processed"
            )
            with open(filename + TXT_EXT, "w") as f:
                f.write(f"[WARNING]: something went wrong analyzing this video\n")
        else:
            log.warning(f"Something went wrong analyzing {filename}{VID_EXT}")


async def run(*args, _filename=None):
    if not _filename:
        return await asyncio.create_subprocess_exec(*args)
    p = await asyncio.create_subprocess_exec(*args)
    await p.wait()
    if p.returncode:
        cleanup(_filename)


async def main():
    proc = await run(
        "inotifywait", "-m", "-r", "-e", "close_write", "--format", "%w%f", RECORDINGS
    )

    while True:
        recording = (await proc.stdout.readline()).rstrip()

        if recording.endswith(VID_EXT) or recording.endswith(f"{VID_EXT}-merged"):
            filename = os.path.splitext(recording)[0]
        elif recording.endswith(CHP_EXT):
            filename = recording.rpartition(CHP_EXT)[0]
        else:
            if recording.endswith(".log.txt"):
                log.info(recording)
            continue

        if recording.endswith(VID_EXT):
            if not os.path.exists(recording) or not os.path.isfile(recording):
                log.error(f"Unable to find {recording}")
                continue
            elif os.path.exists(filename + TXT_EXT):
                log.info(f"[0/0] {recording} already processed")
                continue

            log.info(f'[1/3] Recording FILENAME="{recording}" ended')
            command = list(_nice)
            command += ["comskip", f"--ini={COMSKIP_INI}", "--hwassist", "-d", "70", recording, _filename=filename]
            await run(command)

        elif recording.endswith(CHP_EXT):
            chapters = recording
            merged = filename + MRG_EXT
            recording = filename + VID_EXT
            if not os.path.exists(chapters) or os.path.getsize(chapters) == 132:
                log.warning("No commercials found, skipping...")
                cleanup(filename, _check=False)
                continue
            log.info(f'[2/3] Chapters FILENAME="{chapters}" generated')
            command = list(_nice)
            command += [LOCK_MKVMERGE, "mkvmerge", "-o", merged]
            command += ["--chapters", chapters, recording, _filename=filename]
            await run(command)

        elif recording.endswith(MRG_EXT):
            merged = recording
            recording = filename + VID_EXT
            log.info(f'[3/3] Commercial cutpoints FILENAME="{merged}" merged succesfully')
            try:
                os.rename(merged, recording)
            except:
                log.error(f'[Could not move "{merged}" to "{recording}"')
            cleanup(filename)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.info("Good bye!")
finally:
    for file in (LOCK_COMSKIP, LOCK_MKVMERGE):
        if os.path.exists(file):
            os.remove(file)
