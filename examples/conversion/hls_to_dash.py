"""
examples.conversion.hls_to_dash
~~~~~~~~~~~~

Convert HLS stream to DASH stream


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import sys
import logging

import ffmpeg_streaming
from ffmpeg_streaming import Representation

logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')


def progress(per, ffmpeg):
    sys.stdout.write("\n%s%% - %s" % (per, ffmpeg))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help='A URL to HLS manifest e.x. http://website.com/hls-manifest.m3u8 (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')
    args = parser.parse_args()

    r_360p = Representation(width=640, height=360, kilo_bitrate=276)

    (
        ffmpeg_streaming
            .dash(args.input)
            .format('libx265')
            .add_rep(r_360p)
            .package(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
