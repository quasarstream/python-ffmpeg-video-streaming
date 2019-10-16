"""
examples.hls.hls_encryption
~~~~~~~~~~~~

Create encrypted HlS streams and manifests


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import sys
import ffmpeg_streaming


def transcode_progress(percentage, ffmpeg):
    # You can update a field in your database(or log it)
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-key', '--key', required=True, help='The full pathname of the file where a random key will '
                                                             'be created (required). Note: The path of the key should '
                                                             'be accessible from your website(e.g. '
                                                             '"/var/www/public_html/keys/enc.key")')
    parser.add_argument('-url', '--url', required=True, help='A URL (or a path) to access the key on your website ('
                                                             'required). It is highly recommended to protect the key '
                                                             'on your website(e.g using a token or check a '
                                                             'session/cookie)')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    args = parser.parse_args()

    (
        ffmpeg_streaming
            .hls(args.input)
            .encryption(args.key, args.url)
            .format('libx264')
            .auto_rep()
            .package(args.output, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
