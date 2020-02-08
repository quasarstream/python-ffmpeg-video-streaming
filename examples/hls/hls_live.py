"""
examples.hls.hls_live
~~~~~~~~~~~~

Upload HlS files to a server


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
    parser.add_argument('-m', '--master_playlist', required=True,
                        help='The path to write the master playlist (required).')
    parser.add_argument('-o', '--output', required=True,
                        help='A URL(or a supported resource e.x. http://website.com/live-out.m3u8) to upload files.')
    args = parser.parse_args()

    (
        ffmpeg_streaming
            .hls(args.input, master_playlist_path=args.master_playlist)
            .format('libx264')
            .auto_rep()
            .package(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
