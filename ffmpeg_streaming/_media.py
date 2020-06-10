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
import asyncio

from ._clouds import CloudManager
from ._command_builder import command_builder
from ._format import Format
from ._hls_helper import HLSKeyInfoFile, HLSMasterPlaylist
from ._process import Process
from ._reperesentation import Representation, AutoRep
from ._utiles import mkdir, rm
from .ffprobe import FFProbe


class Save(abc.ABC):
    def __init__(self, media, _format: Format, **options):
        """
        @TODO: add documentation
        """
        atexit.register(self.finish_up)

        self.output_ = ''
        self.key = None
        self.media = media
        self.format = _format
        self.options = options
        self.pipe = None
        self.probe = None
        self.output_temp = False

    def finish_up(self):
        """
        @TODO: add documentation
        """
        if self.media.input_temp:
            rm(self.media.input)
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
        """
        @TODO: add documentation
        """
        if output is None and clouds is None:
            self.output_ = self.media.input
        elif clouds is not None:
            self.output_temp = True
            if clouds.filename is None:
                clouds.filename = os.path.basename(output if output is not None else self.media.input)
            self.output_ = os.path.join(tempfile.mkdtemp(prefix='ffmpeg_streaming_'), clouds.filename)
        else:
            mkdir(os.path.dirname(output))
            self.output_ = output

        self.set_up()
        asyncio.run(self._run(ffmpeg_bin, monitor, **options))

        if clouds is not None:
            clouds.transfer('upload_directory', os.path.dirname(self.output_))

        if output is not None and self.output_temp:
            shutil.move(os.path.dirname(self.output_), os.path.dirname(output))

    async def _run(self, ffmpeg_bin, monitor: callable = None, **options):
        """
        @TODO: add documentation
        """
        with Process(self, command_builder(ffmpeg_bin, self), monitor, **options) as process:
            self.pipe, err = process.run()


class Streaming(Save, abc.ABC):
    def __init__(self, media, _format: Format, **options):
        """
        @TODO: add documentation
        """
        self.reps = list
        super(Streaming, self).__init__(media, _format, **options)

    def representations(self, *reps: Representation):
        self.reps = list(reps)

    def auto_generate_representations(self, heights=None, bitrate=None, ffprobe_bin='ffprobe', include_original=True):
        """
        @TODO: add documentation
        """
        self.probe = FFProbe(self.media.input, ffprobe_bin)
        self.reps = AutoRep(self.probe.video_size, self.probe.bitrate, self.format, heights, bitrate, include_original)

    def add_filter(self, *_filter: str):
        """
        @TODO: add documentation
        """
        _filters = self.options.pop('filter_complex', None)
        _filters = _filters + "," + ",".join(list(_filter)) if _filters is not None else ",".join(list(_filter))
        self.options.update({'filter_complex': _filters})

    def watermarking(self, path, _filter='overlay=10:10'):
        """
        @TODO: add documentation
        """
        self.media.inputs.input(path)
        self.add_filter(_filter)


class DASH(Streaming):
    def set_up(self):
        pass

    def generate_hls_playlist(self):
        self.options.update({'hls_playlist': 1})


class HLS(Streaming):
    KEY_INFO_FILE_PATH = None
    PERIODIC_RE_KEY_FLAG = 'periodic_rekey'
    MASTER_PLAYLIST_IS_SAVED = False

    def set_up(self):
        """
        @TODO: add documentation
        """
        if not HLS.MASTER_PLAYLIST_IS_SAVED:
            self.save_master_playlist()

    def encryption(self, path: str, url: str, key_rotation_period: int = 0, needle: str = ".ts' for writing", length: int = 16):
        """
        @TODO: add documentation
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='_py_ff_vi_st.tmp', delete=False) as key_info:
            HLS.KEY_INFO_FILE_PATH = key_info.name

        key_info_file = HLSKeyInfoFile(HLS.KEY_INFO_FILE_PATH, path, url, key_rotation_period, needle, length)
        self.options.update({'hls_key_info_file': str(key_info_file)})

        if key_rotation_period > 0:
            setattr(self, 'key_rotation', key_info_file)
            self.flags(HLS.PERIODIC_RE_KEY_FLAG)

    def fragmented_mp4(self):
        """
        @TODO: add documentation
        """
        self.options.update({'hls_segment_type': 'fmp4'})

    def save_master_playlist(self, path=None):
        """
        @TODO: add documentation
        """
        if path is not None:
            HLS.MASTER_PLAYLIST_IS_SAVED = True

        HLSMasterPlaylist.generate(self, path)

    def flags(self, *flags: str):
        """
        @TODO: add documentation
        """
        hls_flags = self.options.pop('hls_flags', None)
        hls_flags = hls_flags + "+" + "+".join(list(flags)) if hls_flags is not None else "+".join(list(flags))
        self.options.update({'hls_flags': hls_flags})

    def finish_up(self):
        """
        @TODO: add documentation
        """
        if HLS.KEY_INFO_FILE_PATH is not None:
            rm(HLS.KEY_INFO_FILE_PATH)

        super(HLS, self).finish_up()


class Stream2File(Save):
    """
    @TODO: add documentation
    """
    def set_up(self):
        pass


class Media(object):
    def __init__(self, _inputs):
        """
        @TODO: add documentation
        """
        self.inputs = _inputs

        first_options = dict(_inputs.inputs[0])
        self.input = first_options.get('i', None)
        self.input_temp = first_options.get('is_tmp', False)

    def hls(self, _format: Format, **hls_options):
        """
        @TODO: add documentation
        """
        return HLS(self, _format, **hls_options)

    def dash(self, _format: Format, **dash_options):
        """
        @TODO: add documentation
        """
        return DASH(self, _format, **dash_options)

    def stream2file(self, _format: Format, **options):
        """
        @TODO: add documentation
        """
        return Stream2File(self, _format, **options)

