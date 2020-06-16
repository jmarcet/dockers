#!/usr/local/bin/python3.8 -u

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


def log(text):
    print(text)
    with open(LOGFILE, 'a') as f:
        f.write(f'{text}\n')


def cleanup(filename, _check=True):
    [os.remove(x) for x in glob(filename + b'.*') if not x.endswith(b'.txt') and not x.endswith(b'.mpeg')]
    if _check and (not os.path.exists(filename + b'.txt') or not os.path.getsize(filename + b'.txt')):
        if os.path.exists(filename + b'.mpeg'):
            log(f'[WARNING]: something went wrong analyzing {filename}.mpeg, marking as already processed')
            with open(filename + b'.txt', 'w') as f:
                f.write(f'[WARNING]: something went wrong analyzing this video\n')
        else:
            log(f'[WARNING]: something went wrong analyzing {filename}.mpeg')


async def run(*args, _filename=None):
    if not _filename:
        return await asyncio.create_subprocess_exec(*args, stdout=PIPE)
    p = await asyncio.create_subprocess_exec(*args)
    await p.wait()
    if p.returncode != 0:
        cleanup(_filename)


async def main():
    proc = await run(INOTIFYWAIT, '-m', '-r', '-e', 'close_write', '--format', '%w%f', RECORDINGS)

    while True:
        recording = (await proc.stdout.readline()).rstrip()

        if recording.endswith(b'.mpeg') or recording.endswith(b'.mpeg-merged'):
            filename = os.path.splitext(recording)[0]
        elif recording.endswith(b'.mkvtoolnix.chapters'):
            filename = recording.rpartition(b'.mkvtoolnix.chapters')[0]
        else:
            if recording.endswith(b'.log.txt'):
                log(recording)
            continue

        if recording.endswith(b'.mpeg'):
            if not os.path.exists(recording) or not os.path.isfile(recording):
                log(f'[ERROR] unable to find {recording}')
                continue
            elif os.path.exists(filename + b'.txt'):
                log(f'[0/0] {recording} already processed')
                continue

            log(f'[1/3] Recording FILENAME="{recording}" ended')
            await run(NICE, '-n', '15', IONICE, '-c', '3',
                      COMSKIP, f'--ini={COMSKIP_INI}', recording, _filename=filename)

        elif recording.endswith(b'.mkvtoolnix.chapters'):
            chapters = recording
            merged = filename + b'.mpeg-merged'
            recording = filename + b'.mpeg'
            if not os.path.exists(chapters) or os.path.getsize(chapters) == 132:
                log('[WARNING] No commercials found, skipping...')
                cleanup(filename, _check=False)
                continue
            log(f'[2/3] Chapters FILENAME="{chapters}" generated')
            await run(NICE, '-n', '15', IONICE, '-c', '3',
                      MKVMERGE, '-o', merged, '--chapters', chapters, recording, _filename=filename)

        elif recording.endswith(b'.mpeg-merged'):
            merged = recording
            recording = filename + b'.mpeg'
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
