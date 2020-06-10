"""
examples.dash
~~~~~~~~~~~~

Create DASH streams and manifest


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


def monitor(ffmpeg, duration, time_, process):
    # You can update a field in your database or log it to a file
    # You can also create a socket connection and show a progress bar to users
    # logging.info(ffmpeg) or print(ffmpeg)

    # if "something happened":
    #     process.terminate()

    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s [%s%s]" % (per, time_left(time_, duration), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    parser.add_argument('-hls', '--hls_output', default=False, help='publish hls playlists')

    args = parser.parse_args()

    video = ffmpeg_streaming.input(args.input)

    dash = video.dash(Formats.h264())
    dash.auto_generate_representations()

    if args.hls_output:
        dash.generate_hls_playlist()

    dash.output(args.output, monitor=monitor)


if __name__ == "__main__":
    sys.exit(main())
