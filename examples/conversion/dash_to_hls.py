"""
examples.conversion.dash_to_hls
~~~~~~~~~~~~

Convert DASH stream to HLS stream


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import sys
import logging

import ffmpeg_streaming


logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')


def progress(per, ffmpeg):
    sys.stdout.write("\n%s%% - %s" % (per, ffmpeg))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help='A URL to DASH manifest e.x. http://website.com/dash-manifest.mpd (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')
    args = parser.parse_args()

    (
        ffmpeg_streaming
            .hls(args.input)
            .format('libx264')
            .auto_rep(heights=[360, 240])
            .package(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
