"""
examples.dash.dash
~~~~~~~~~~~~

Create DASH streams and manifest


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


start_time = time.time()
logging.basicConfig(filename='Transcoding-' + str(start_time) + '.log', level=logging.DEBUG)


def per_to_time_left(percentage):
    if percentage != 0:
        diff_time = time.time() - start_time
        seconds_left = 100 * diff_time / percentage - diff_time
        time_left = str(datetime.timedelta(seconds=int(seconds_left))) + ' left'
    else:
        time_left = 'calculating...'

    return time_left


def transcode_progress(per, ffmpeg):
    # You can update a field in your database or can log it to a file
    # You can also create a socket connection and show a progress bar to users
    logging.debug(ffmpeg)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    args = parser.parse_args()

    logging.debug("input: " + args.input
                  + ", output: " + str(args.output)
                  + ", datetime: " + str(datetime.datetime.now()))
    (
        ffmpeg_streaming
            .dash(args.input, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package(args.output, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
