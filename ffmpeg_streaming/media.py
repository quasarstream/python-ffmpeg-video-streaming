"""
ffmpeg_streaming.media
~~~~~~~~~~~~

Media object to build a stream objects


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import os
import shutil
import tempfile

from ffmpeg_streaming.build_commands import build_command
from ffmpeg_streaming.clouds import open_from_cloud, save_to_clouds
from ffmpeg_streaming.export_hls_playlist import export_hls_playlist
from ffmpeg_streaming.utiles import get_path_info, clear_tmp_file
from .key_info_file import generate_key_info_file
from .process import Process
from ._ffprobe import *
from .auto_rep import AutoRepresentation


def _get_paths(output, _input, clouds):
    is_tmp = False

    if output is not None:
        dirname, name = get_path_info(output)
    else:
        dirname, name = get_path_info(_input)
        output = _input
    if clouds is not None:
        is_tmp = True
        basename = os.path.basename(output)
        output = os.path.join(tempfile.mkdtemp(suffix='ffmpeg_streaming'), basename)
        dirname, name = get_path_info(output)

    return output, dirname, name, is_tmp


class Export(object):
    video_format = str
    audio_format = str
    reps = list
    output = str
    _is_tmp_directory = False

    def __init__(self, filename, options):
        self.filename = filename
        self.options = options

    def __del__(self):
        clear_tmp_file(self.filename)
        if isinstance(self, HLS):
            clear_tmp_file(self.hls_key_info_file)
        if Export._is_tmp_directory:
            shutil.rmtree(os.path.dirname(str(Export.output)), ignore_errors=True)

    def add_rep(self, *args):
        Export.reps = list(args)
        return self

    def auto_rep(self, heights=None, cmd='ffprobe'):
        Export.reps = AutoRepresentation(ffprobe(self.filename, cmd), heights).generate()
        return self

    def format(self, video, audio=None):
        Export.video_format = video
        Export.audio_format = audio
        return self

    def package(
            self,
            output=None,
            clouds=None,
            progress=None,
            cmd='ffmpeg',
            c_stdout=False,
            c_stderr=True,
            c_stdin=True,
            c_input=None,
            timeout=None
         ):
        Export.output, dirname, name, Export._is_tmp_directory = _get_paths(output, self.filename, clouds)

        if isinstance(self, HLS):
            export_hls_playlist(dirname, name, Export.reps)

        with Process(self, progress, build_command(cmd, self), c_stdout, c_stderr, c_stdin) as process:
            p = process.run(c_input, timeout)

        save_to_clouds(clouds, dirname)

        if output is not None and clouds is not None:
            shutil.move(dirname, os.path.dirname(output))

        return p


class HLS(Export):

    def __init__(self, filename, options):
        self.hls_time = options.pop('hls_time', 10)
        self.hls_allow_cache = options.pop('hls_allow_cache', 0)
        self.hls_key_info_file = options.pop('hls_key_info_file', None)
        super(HLS, self).__init__(filename, options)

    def encryption(self, url, path, length=16):
        self.hls_key_info_file = generate_key_info_file(url, path, length)
        return self


class DASH(Export):

    def __init__(self, filename, options):
        self.adaption = options.pop('adaption', None)
        super(DASH, self).__init__(filename, options)


def _check_file(file):
    if type(file) == tuple:
        file = open_from_cloud(file)

    if not os.path.isfile(file):
        raise RuntimeError('The file is not exist')

    return file


def dash(file, **kwargs):
    return DASH(_check_file(file), kwargs)


def hls(file, **kwargs):
    return HLS(_check_file(file), kwargs)


__all__ = [
    'dash',
    'hls'
]
