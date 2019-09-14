import os

from ffmpeg_streaming.export_hls_playlist import export_hls_playlist
from ffmpeg_streaming.utiles import get_path_info
from .key_info_file import generate_key_info_file
from .process import run
from ._ffprobe import *
from .auto_rep import AutoRepresentation


class Export(object):
    video_format = str
    audio_format = str
    reps = list
    output = str

    def __init__(self, filename, options):
        self.filename = filename
        self.options = options

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
            progress=None,
            cmd='ffmpeg',
            capture_stdout=False,
            capture_stderr=True,
            input=None,
            timeout=None
         ):
        if output is None:
            Export.output = self.filename
        else:
            Export.output = output

        if isinstance(self, HLS):
            dirname, name = get_path_info(Export.output)
            export_hls_playlist(dirname, name, Export.reps)

        return run(self, progress, cmd, capture_stdout, capture_stderr, input, timeout)


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


def dash(filename, **kwargs):
    if not os.path.isfile(filename):
        raise RuntimeError('The file is not exist')
    return DASH(filename, kwargs)


def hls(filename, **kwargs):
    if not os.path.isfile(filename):
        raise RuntimeError('The file is not exist')
    return HLS(filename, kwargs)


__all__ = [
    'dash',
    'hls'
]
