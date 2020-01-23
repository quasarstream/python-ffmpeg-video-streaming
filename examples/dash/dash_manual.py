"""
examples.dash.dash_manual
~~~~~~~~~~~~

Create DASH files in the resolutions that you have specified


:copyright: (c) 2019 by Amin Yazdanpanah.
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

from ffmpeg_streaming import Representation

logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')
start_time = time.time()


def per_to_time_left(percentage):
    if percentage != 0:
        diff_time = time.time() - start_time
        seconds_left = 100 * diff_time / percentage - diff_time
        time_left = str(datetime.timedelta(seconds=int(seconds_left))) + ' left'
    else:
        time_left = 'calculating...'

    return time_left


def transcode_progress(per, ffmpeg):
    # You can update a field in your database or log it to a file
    # You can also create a socket connection and show a progress bar to users
    logging.info(ffmpeg)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    args = parser.parse_args()

    rep1 = Representation(width=256, height=144, kilo_bitrate=200, audio_k_bitrate=64)
    rep2 = Representation(width=854, height=480, kilo_bitrate=500, audio_k_bitrate=128)
    rep3 = Representation(width=1080, height=720, kilo_bitrate=1000, audio_k_bitrate=320)

    (
        ffmpeg_streaming
            .dash(args.input, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .add_rep(rep1, rep2, rep3)
            .package(args.output, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
