"""
examples.dash.dash_live
~~~~~~~~~~~~

Upload DASH streams and manifest to a server


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
                        help='The path to the video file(or a supported resource) (required).')
    parser.add_argument('-o', '--output', required=True,
                        help='A URL(or a supported resource e.x. http://website.com/live-out.mpd) to upload files.')
    args = parser.parse_args()

    (
        ffmpeg_streaming
            .dash(args.input, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .live(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
