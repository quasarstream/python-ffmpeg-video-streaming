"""
examples.hls
~~~~~~~~~~~~

Create HlS streams


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import datetime
import sys
import time
import logging

import ffmpeg_streaming
from ffmpeg_streaming import Formats

logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')
start_time = time.time()


def time_left(time_, total):
    if time_ != 0:
        diff_time = time.time() - start_time
        seconds_left = total * diff_time / time_ - diff_time
        time_left = str(datetime.timedelta(seconds=int(seconds_left))) + ' left'
    else:
        time_left = 'calculating...'

    return time_left


def monitor(ffmpeg, duration, time_):
    # You can update a field in your database or log it to a file
    # You can also create a socket connection and show a progress bar to users
    # logging.info(ffmpeg)
    per = round(time_ / duration * 100)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, time_left(time_, duration), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    parser.add_argument('-k', '--key', default=None, help='The full pathname of the file where a random key will '
                                                             'be created (required). Note: The path of the key should'
                                                             'be accessible from your website(e.g. '
                                                             '"/var/www/public_html/keys/enc.key")')
    parser.add_argument('-u', '--url', default=None, help='A URL (or a path) to access the key on your website ('
                                                          'required)')

    args = parser.parse_args()

    video = ffmpeg_streaming.input(args.input)

    hls = video.hls(Formats.h264())
    hls.auto_generate_representations()

    if args.key is not None and args.url is not None:
        hls.encryption(args.key, args.url, 10)

    hls.output(args.output, monitor=monitor)


if __name__ == "__main__":
    sys.exit(main())
