#!/usr/bin/env python3

import multiprocessing.pool
import subprocess

ARGS_FILE_NAME = '.youtube-archive'

USAGE = """\
Usage: {0} [SEARCH OPTIONS] [-- [DOWNLOAD OPTIONS]]
OPTIONS are passed to youtube-dl for finding videos
DOWNLOAD OPTIONS are passed to youtube-dl when downloading a video

Arguments are stored in """ + ARGS_FILE_NAME + """ in JSON format. To re-invoke
youtube-archiver (to update your archive), start this program with no
arguments. If you wish to change the arguments, either modify the file or
delete it, and provide them as command-line arguments. This program will not
accept command-line arguments while the argument file is present.

See youtube-dl documentation.

Examples:

{0} https://www.youtube.com/user/YouTube -- --extract-audio
{0} https://www.youtube.com/user/YouTube --match-title 2016
"""

YTD_PATH = 'youtube-dl'

YTD_SEARCH_ARGS = [
    '--get-id',                                # List IDS instead of downloading
    '--ignore-errors',                         # Continue if video is blocked
]

YTD_DOWNLOAD_ARGS = [
    '--add-metadata',
    '--download-archive', 'yt-archive.txt',    # Don't redownload files
    '--embed-subs',
    '--write-annotations',
    '--write-description',
    '--write-info-json',
    '--write-thumbnail',
    '--xattrs',
]


def assigner(workloader, worker, max_workers=4):
    assert(workloader.stdout.readable())
    tp = multiprocessing.pool.ThreadPool(max_workers)
    for num, line in enumerate(workloader.stdout):
        ytid = line[:-1].decode('utf-8')
        print('Assigning worker {} to video {} ...'.format(num, ytid))
        tp.apply_async(worker, (ytid, num))
    tp.close()
    print('All workers assigned')
    tp.join()


def archive(user_search_args, user_download_args=[], threads=4):
    search_call = [YTD_PATH] + YTD_SEARCH_ARGS + user_search_args
    dl_call_start = [YTD_PATH] + user_download_args + YTD_DOWNLOAD_ARGS

    search_process = subprocess.Popen(search_call, stdout=subprocess.PIPE)

    def downloader(ytid, num=1):
        url = "https://www.youtube.com/watch?v={}".format(ytid)
        extra_args = ['--autonumber-start', str(num), url]
        print(' '.join(dl_call_start + extra_args))
        subprocess.call(dl_call_start + extra_args)

    assigner(search_process, downloader, threads)


def main(args):
    if '--' in args:
        index = args.index('--')
        user_search_args = args[:index]
        user_download_args = args[index+1:]
        archive(user_search_args, user_download_args)
    else:
        archive(args)


if __name__ == '__main__':
    import sys
    import os.path
    import json

    if os.path.exists(ARGS_FILE_NAME) and len(sys.argv) == 1:
        with open(ARGS_FILE_NAME) as f:
            args = json.load(f)
    elif not os.path.exists(ARGS_FILE_NAME) and len(sys.argv) > 1:
        args = sys.argv[1:]
        with open(ARGS_FILE_NAME, 'w') as f:
            json.dump(args, f)
    elif len(sys.argv) == 1:
        print(USAGE.format(sys.argv[0]))
        sys.exit(1)
    else:
        print("Detected {} already exists.".format(ARGS_FILE_NAME))
        print("Either delete it or do not supply command-line arguments.")
        sys.exit(1)

    main(args)
