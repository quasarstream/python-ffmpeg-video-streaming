from ffmpeg_streaming.key_info_file import generate_key_info_file
from .process import run
from ._ffprobe import *
from .auto_rep import AutoRepresentation


class Export(object):
    def __init__(self, filename):
        self.reps = None
        self.filename = filename

    def add_rep(self, *args):
        self.reps = list(args)
        return self

    def auto_rep(self, heights=None, cmd='ffprobe'):
        self.reps = AutoRepresentation(FFProbe(self.filename, cmd), heights).generate()
        return self

    def format(self, video_format):
        self.format = video_format
        return self

    def package(
            self,
            path=None,
            progress=None,
            cmd='ffmpeg',
            ffprobe_cmd='ffprobe',
            capture_stdout=False,
            capture_stderr=False,
            input=None,
            timeout=None
         ):
        if path is None:
            self.path = self.filename
        else:
            self.path = path

        return run(self, progress, cmd, ffprobe_cmd, capture_stdout, capture_stderr, input, timeout)


class HLS(Export):

    def __init__(self, filename, kwargs):
        self.hls_time = kwargs.pop('hls_time', 10)
        self.hls_allow_cache = kwargs.pop('hls_allow_cache', 0)
        self.strict = kwargs.pop('strict', "-2")
        self.hls_key_info_file = kwargs.pop('hls_key_info_file', None)
        self.filter = kwargs
        super(HLS, self).__init__(filename)

    def encryption(self, url, path, length=16):
        self.hls_key_info_file = generate_key_info_file(url, path, length)
        return self


class DASH(Export):

    def __init__(self, filename, kwargs):
        self.adaption = kwargs.pop('adaption', None)
        self.strict = kwargs.pop('strict', "-2")
        self.filter = kwargs
        super(DASH, self).__init__(filename)


__all__ = [
    'HLS',
    'DASH'
]