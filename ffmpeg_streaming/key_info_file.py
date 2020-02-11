"""
ffmpeg_streaming.key_info_file
~~~~~~~~~~~~

Generate a random key and key info file to pass to the FFmpeg to create encrypted HLS streams


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import tempfile
from secrets import token_bytes, token_hex


def generate_key_info_file(url, path, key_info_path=None, length=16):
    with open(path, 'wb') as key:
        key.write(token_bytes(length))

    if key_info_path is None:
        _key_info_file = tempfile.NamedTemporaryFile(mode='w', suffix='_py_ff_vi_st.tmp', delete=False)
    else:
        _key_info_file = open(key_info_path, mode="w")

    with _key_info_file as key_info:
        key_info.write("\n".join([url, path, token_hex(length)]))
    return key_info.name


__all__ = [
    'generate_key_info_file',
]
