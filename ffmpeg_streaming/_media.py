"""
ffmpeg_streaming.media
~~~~~~~~~~~~

Media object to build a stream objects


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import abc
import os
import shutil
import tempfile
import atexit
from abc import ABC

from ._clouds import CloudManager
from ._command_builder import command_builder
from ._format import Format
from ._hls_helper import HLSKeyInfoFile, HLSMasterPlaylist
from ._process import Process
from ._reperesentation import Representation, AutoRep
from ._utiles import mkdir
from .ffprobe import FFProbe


class Save(abc.ABC):
    def __init__(self, media, _format: Format, **options):
        atexit.register(self.finish_up)

        self.output_ = ''
        self.key = None
        self.media = media
        self.format = _format
        self.options = options
        self.pipe = None
        self.output_temp = False

    def finish_up(self):
        if self.media.input_temp:
            os.remove(self.media.input)
        if self.output_temp:
            shutil.rmtree(os.path.dirname(str(self.output_)), ignore_errors=True)

    @abc.abstractmethod
    def set_up(self):
        pass

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name in ['save', 'package']:
                self.output(*args, **kwargs)
            else:
                raise AttributeError("The object has no attribute {}".format(name))

        return method

    def output(self, output: str = None, clouds: CloudManager = None, monitor: callable = None, ffmpeg_bin: str = 'ffmpeg', **options):
        if output is None and clouds is None:
            self.output_ = self.media.input
        elif clouds is not None:
            self.output_temp = True
            basename = os.path.basename(output if output is not None else self.media.input)
            self.output_ = os.path.join(tempfile.mkdtemp(prefix='ffmpeg_streaming_'), basename)
        else:
            mkdir(os.path.dirname(output))
            self.output_ = output
        self.set_up()
        self._run(ffmpeg_bin, monitor, **options)
        if clouds is not None:
            clouds.transfer('upload_directory', os.path.dirname(self.output_))

        if output is not None and self.output_temp:
            shutil.move(os.path.dirname(self.output_), os.path.dirname(output))

    def _run(self, ffmpeg_bin, monitor: callable = None, **options):
        with Process(self, command_builder(ffmpeg_bin, self), monitor, **options) as process:
            self.pipe, err = process.run()


class Streaming(Save, ABC):
    def __init__(self, media, _format: Format, **options):
        self.reps = list
        super(Streaming, self).__init__(media, _format, **options)

    def representations(self, *reps: Representation):
        self.reps = list(reps)

    def auto_generate_representations(self, heights=None, bitrate=None, ffprobe_bin='ffprobe'):
        probe = FFProbe(self.media.input, ffprobe_bin)
        self.reps = AutoRep(probe.video_size, probe.bitrate, self.format, heights, bitrate)


class DASH(Streaming):
    def set_up(self):
        pass

    def generate_hls_playlist(self):
        self.options.update({'hls_playlist': "1"})


class HLS(Streaming):
    KEY_INFO_FILE_PATH = None

    def set_up(self):
        HLSMasterPlaylist.generate(self)

    def encryption(self, path: str, url: str, key_rotation_period: int = 0, needle: str = ".ts' for writing", length: int = 16):
        with tempfile.NamedTemporaryFile(mode='w', suffix='_py_ff_vi_st.tmp', delete=False) as key_info:
            HLS.KEY_INFO_FILE_PATH = key_info.name

        key_info_file = HLSKeyInfoFile(HLS.KEY_INFO_FILE_PATH, path, url, key_rotation_period, needle, length)
        self.options.update({'hls_key_info_file': str(key_info_file)})
        if key_rotation_period > 0:
            setattr(self, 'key_rotation', key_info_file)
            self.flags('periodic_rekey')

    def fragmented_mp4(self):
        self.options.update({'hls_segment_type': 'fmp4'})

    def flags(self, *flags: str):
        hls_flags = self.options.pop('hls_flags', None)
        hls_flags = hls_flags + "+" + "+".join(list(flags)) if hls_flags is not None else "+".join(list(flags))
        self.options.update({'hls_flags': hls_flags})

    def finish_up(self):
        if HLS.KEY_INFO_FILE_PATH is not None:
            shutil.rmtree(HLS.KEY_INFO_FILE_PATH, ignore_errors=True)

        super(HLS, self).finish_up()


class Stream2File(Save):
    def set_up(self):
        pass


class Media(object):
    def __init__(self, input_opts):
        options = dict(input_opts)
        self.input = options.get('i', None)
        self.input_temp = options.pop('is_tmp', False)
        self.input_opts = options

    def hls(self, _format: Format, **options):
        return HLS(self, _format, **options)

    def dash(self, _format: Format, **options):
        return DASH(self, _format, **options)

    def stream2file(self, _format: Format, **options):
        return Stream2File(self, _format, **options)

