"""
examples.conversion.stream_to_file
~~~~~~~~~~~~

Convert a stream(DASH or HLS) to File


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
                        help='A URL to a stream manifest (HLS or DASH) (required).')
    parser.add_argument('-o', '--output', default=None,
                        help='The output to write a file. e.x. /var/www/media/new-video.mp4')
    args = parser.parse_args()

    (
        ffmpeg_streaming
            .stream2file(args.input)
            .format('libx264')
            .save(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
