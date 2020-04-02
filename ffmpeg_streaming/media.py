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
from ffmpeg_streaming.utiles import get_path_info, clear_tmp_file, is_url
from .key_info_file import generate_key_info_file
from .process import Process
from ._ffprobe import *
from .auto_rep import AutoRepresentation


def _get_paths(output, _input, clouds):
    is_tmp = False
    if clouds is not None:
        is_tmp = True
        basename = os.path.basename(output if output is not None else _input)
        output = os.path.join(tempfile.mkdtemp(prefix='ffmpeg_streaming_'), basename)
        dirname, name = get_path_info(output)
    elif output is not None:
        dirname, name = get_path_info(output)
    else:
        dirname, name = get_path_info(_input)
        output = _input

    return output, dirname, name, is_tmp


def _save_hls_master_playlist(output, master_playlist_path, dirname, name):
    if is_url(output):
        if master_playlist_path is None:
            raise ValueError("You must specify a path for master playlist")
        playlist_path = master_playlist_path
    else:
        playlist_path = dirname + "/" + name + ".m3u8"
    export_hls_playlist(playlist_path, name, Export.reps)


class Export(object):
    video_format = str
    audio_format = str
    _ffprobe = None
    _ffmpeg = None
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

    def __getattr__(self, name):
        def method(*args, **kwargs):
            # TODO: implement save and live methods in the future
            if name in ['save', 'live']:
                self.package(*args, **kwargs)
            else:
                raise AttributeError("The object has no attribute {}".format(name))

        return method

    def add_rep(self, *args):
        Export.reps = list(args)
        return self

    def auto_rep(self, heights=None, cmd='ffprobe'):
        Export._ffprobe = ffprobe(self.filename, cmd)
        Export.reps = AutoRepresentation(Export._ffprobe, heights).generate()
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
            _save_hls_master_playlist(output, self.master_playlist_path, dirname, name)

        with Process(progress, build_command(cmd, self), c_stdout, c_stderr, c_stdin) as process:
            Export._ffmpeg = process.run(c_input, timeout)

        save_to_clouds(clouds, dirname)

        if output is not None and clouds is not None:
            shutil.move(dirname, os.path.dirname(output))

        return self


class HLS(Export):

    def __init__(self, filename, **options):
        self.hls_time = options.pop('hls_time', 10)
        self.hls_allow_cache = options.pop('hls_allow_cache', 0)
        self.hls_list_size = options.pop('hls_list_size', 0)
        self.master_playlist_path = options.pop('master_playlist_path', 0)
        self.hls_key_info_file = options.pop('hls_key_info_file', None)
        super(HLS, self).__init__(filename, options)

    def encryption(self, url, path, key_info_path=None, length=16):
        self.hls_key_info_file = generate_key_info_file(url, path, key_info_path, length)
        return self


class DASH(Export):

    def __init__(self, filename, **options):
        self.adaption = options.pop('adaption', None)
        self.init_seg_name = options.pop('init_seg_name', None)
        self.media_seg_name = options.pop('media_seg_name', None)
        super(DASH, self).__init__(filename, options)


class StreamToFile(Export):

    def __init__(self, filename, **options):
        super(StreamToFile, self).__init__(filename, options)


def _check_file(file):
    if type(file) == tuple:
        file = open_from_cloud(file)
    return file


def dash(file, **options):
    return DASH(_check_file(file), **options)


def hls(file, **options):
    return HLS(_check_file(file), **options)


def stream2file(file, **options):
    return StreamToFile(file, **options)


__all__ = [
    'dash',
    'hls',
    'stream2file'
]
