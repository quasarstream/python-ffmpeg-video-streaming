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
import logging
import tempfile
from os.path import join
from random import randrange

import ffmpeg_streaming
from ffmpeg_streaming.key_info_file import generate_key_info_file

logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')

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


key_info_file_path = join(tempfile.gettempdir(), str(randrange(1000, 100000)) + '_py_ff_vi_st.tmp')
k_num = 1


def k_format(name, num):
    return str(name) + "_" + str(num)


def progress(per, ffmpeg):
    global k_num
    if ".ts' for writing" in ffmpeg:
        generate_key_info_file(k_format(args.url, k_num), k_format(args.key, k_num), key_info_path=key_info_file_path)
        k_num += 1


def main():
    (
        ffmpeg_streaming
            .hls(args.input, hls_flags="periodic_rekey")
            .encryption(args.url, args.key, key_info_path=key_info_file_path)
            .format('libx264')
            .auto_rep()
            .package(args.output, progress=progress)
    )


if __name__ == "__main__":
    sys.exit(main())
