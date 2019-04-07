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

    def auto_rep(self, heights=None):
        self.reps = AutoRepresentation(ffprobe(self.filename), heights).generate()
        return self

    def format(self, video_format):
        self.format = video_format
        return self

    def package(
            self,
            path=None,
            cmd='ffmpeg',
            capture_stdout=False,
            capture_stderr=False,
            input=None):
        if path is None:
            self.path = self.filename
        else:
            self.path = path

        return run(self,  cmd, capture_stdout, capture_stderr, input)


class HLS(Export):

    def __init__(self, filename, kwargs):
        self.hls_time = kwargs.pop('hls_time', 10)
        self.hls_allow_cache = kwargs.pop('hls_allow_cache', 0)
        self.hls_key_info_file = kwargs.pop('hls_key_info_file', None)
        super(HLS, self).__init__(filename)


class DASH(Export):

    def __init__(self, filename, kwargs):
        self.adaption = kwargs.pop('adaption', None)
        super(DASH, self).__init__(filename)


__all__ = [
    'HLS',
    'DASH'
]