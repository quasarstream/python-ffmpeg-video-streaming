"""
ffmpeg_streaming.streams
~~~~~~~~~~~~

Useful methods


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import os
import tempfile
import warnings
from urllib.parse import urlparse


def round_to_even(num):
    num = int(num) if ((int(num) % 2) == 0) else int(num) + 1
    return num


def clear_tmp_file(filename):
    if filename is not None and filename.startswith(tempfile.gettempdir()) and filename.endswith('_py_ff_vi_st.tmp'):
        os.remove(filename)


def get_path_info(path):
    dirname = os.path.dirname(path).replace("\\", "/")
    name = str(os.path.basename(path).split('.')[0])

    if not is_url(path) and not os.path.exists(dirname):
        os.makedirs(dirname)

    return dirname, name


def is_url(url):
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])
    except:
        return False


def convert_to_sec(time):
    h, m, s = time.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def deprecated(func):
    def deprecated_fun(*args, **kwargs):
        warnings.warn('The {} method is deprecated and will be removed in a future release'.format(func.__name__)
                      , DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return deprecated_fun
