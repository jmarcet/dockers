#!/usr/local/bin/python3

import asyncio
import os
from asyncio.subprocess import DEVNULL, PIPE
from glob import glob

COMSKIP_INI = '/etc/comskip.ini'
RECORDINGS = os.environ['RECORDINGS']
LOGFILE = os.path.join(RECORDINGS, 'comskip.log')

COMSKIP = 'comskip'
INOTIFYWAIT = 'inotifywait'
IONICE = 'ionice'
MKVMERGE = 'mkvmerge'
NICE = 'nice'
CHP_EXT = ".mkvtoolnix.chapters"
MRG_EXT = ".mkv-merged"
TXT_EXT = ".txt"
VID_EXT = ".mkv"


def log(text):
    print(text)
    with open(LOGFILE, 'a') as f:
        f.write(f'{text}\n')


def cleanup(filename, _check=True):
    [print(x) for x in glob(f"{filename}.*") if os.splitext(x)[1] not in (TXT_EXT, VID_EXT, ".jpg", ".nfo")]
    if _check and (not os.path.exists(filename + TXT_EXT) or not os.path.getsize(filename + TXT_EXT)):
        if os.path.exists(filename + VID_EXT):
            log(f"[WARNING]: something went wrong analyzing {filename}{VID_EXT}, marking as already processed")
            with open(filename + TXT_EXT, 'w') as f:
                f.write(f"[WARNING]: something went wrong analyzing this video\n")
        else:
            log(f"[WARNING]: something went wrong analyzing {filename}{VID_EXT}")


async def run(*args, _filename=None):
    if not _filename:
        return await asyncio.create_subprocess_exec(*args, stdout=PIPE)
    p = await asyncio.create_subprocess_exec(*args)
    await p.wait()
    if p.returncode:
        cleanup(_filename)


async def main():
    proc = await run(INOTIFYWAIT, '-m', '-r', '-e', 'close_write', '--format', '%w%f', RECORDINGS)

    while True:
        recording = (await proc.stdout.readline()).rstrip()

        if recording.endswith(VID_EXT) or recording.endswith(f"{VID_EXT}-merged"):
            filename = os.path.splitext(recording)[0]
        elif recording.endswith(CHP_EXT):
            filename = recording.rpartition(CHP_EXT)[0]
        else:
            if recording.endswith(".log.txt"):
                log(recording)
            continue

        if recording.endswith(VID_EXT):
            if not os.path.exists(recording) or not os.path.isfile(recording):
                log(f"[ERROR] unable to find {recording}")
                continue
            elif os.path.exists(filename + TXT_EXT):
                log(f"[0/0] {recording} already processed")
                continue

            log(f'[1/3] Recording FILENAME="{recording}" ended')
            await run(NICE, "-n", "15", IONICE, "-c", "3", "flock", "/tmp/.comskip.lock",
                      COMSKIP, f"--ini={COMSKIP_INI}", "-d", "70", recording, _filename=filename)

        elif recording.endswith(CHP_EXT):
            chapters = recording
            merged = filename + MRG_EXT
            recording = filename + VID_EXT
            if not os.path.exists(chapters) or os.path.getsize(chapters) == 132:
                log("[WARNING] No commercials found, skipping...")
                cleanup(filename, _check=False)
                continue
            log(f'[2/3] Chapters FILENAME="{chapters}" generated')
            await run(NICE, "-n", "15", IONICE, "-c", '3',
                      MKVMERGE, "-o", merged, "--chapters", chapters, recording, _filename=filename)

        elif recording.endswith(MRG_EXT):
            merged = recording
            recording = filename + VID_EXT
            log(f'[3/3] Commercial cutpoints FILENAME="{merged}" merged succesfully')
            try:
                os.rename(merged, recording)
            except:
                log(f'[ERROR] Could not move "{merged}" to "{recording}"')
            cleanup(filename)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    log('Good bye!')
