"""
ffmpeg_streaming.media
~~~~~~~~~~~~

Video and audio formats


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import abc

MULTIPLY_BY_ONE = 1
MULTIPLY_BY_TWO = 2
MULTIPLY_BY_FOUR = 4
MULTIPLY_BY_Eight = 8
MULTIPLY_BY_SIXTEEN = 16
MULTIPLY_BY_THIRTY_TWO = 32


def _verify_codecs(codec, codecs):
    if codec is None:
        return
    elif codec not in codecs:
        ValueError("The codec is not available!")
    else:
        return str(codec)


class Format(abc.ABC):
    def __init__(self, video: str, audio: str):
        self.video = video
        self.audio = audio

    @abc.abstractmethod
    def multiply(self) -> int:
        pass


class H264(Format):
    def __init__(self, video: str = "libx264", audio: str = 'copy'):
        videos = ['libx264', 'h264', 'h264_afm']
        audios = ['copy', 'aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']

        super(H264, self).__init__(_verify_codecs(video, videos), _verify_codecs(audio, audios))

    def multiply(self) -> int:
        return MULTIPLY_BY_TWO


class HEVC(Format):
    def __init__(self, video: str = "libx265", audio: str = 'copy'):
        videos = ['libx265', 'h265']
        audios = ['copy', 'aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']

        super(HEVC, self).__init__(_verify_codecs(video, videos), _verify_codecs(audio, audios))

    def multiply(self) -> int:
        return MULTIPLY_BY_TWO


class VP9(Format):
    def __init__(self, video: str = "libvpx-vp9", audio: str = 'copy'):
        videos = ['libvpx', 'libvpx-vp9']
        audios = ['copy', 'aac', 'libvo_aacenc', 'libfaac', 'libmp3lame', 'libfdk_aac']

        super(VP9, self).__init__(_verify_codecs(video, videos), _verify_codecs(audio, audios))

    def multiply(self) -> int:
        return MULTIPLY_BY_TWO


class Formats:
    @staticmethod
    def h264(video: str = "libx264", audio: str = 'copy') -> Format:
        return H264(video, audio)

    @staticmethod
    def hevc(video: str = "libx265", audio: str = 'copy') -> Format:
        return HEVC(video, audio)

    @staticmethod
    def vp9(video: str = "libvpx-vp9", audio: str = 'copy') -> Format:
        return VP9(video, audio)


__all__ = [
    'Format',
    'Formats'
]
