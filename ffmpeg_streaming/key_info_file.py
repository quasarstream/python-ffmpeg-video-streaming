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


def generate_key_info_file(url, path, length=16):
    with open(path, 'wb') as key:
        key.write(token_bytes(length))
    with tempfile.NamedTemporaryFile(mode='w', suffix='_py_ff_vi_st.tmp', delete=False) as key_info:
        key_info.write("\n".join([url, path, token_hex(length)]))
    return key_info.name
