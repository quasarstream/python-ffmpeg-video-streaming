"""
ffmpeg_streaming.rep
~~~~~~~~~~~~

Generate Representation object


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""


class Representation:
    def __init__(self, **kwargs):
        self.width = kwargs.pop('width', None)
        self.height = kwargs.pop('height', None)
        self.kilo_bitrate = kwargs.pop('kilo_bitrate', None)
        self.audio_kilo_bitrate = kwargs.pop('audio_k_bitrate', None)

    @property
    def size(self) -> str:
        if self.width is None or self.height is None:
            raise ValueError("You must set the width and the height of video")
        return str(self.width) + "x" + str(self.height)

    @property
    def bit_rate(self) -> str:
        if self.kilo_bitrate is None:
            raise ValueError("You must set the bitrate of video")
        return str(self.kilo_bitrate) + "k"

    @property
    def audio_bit_rate(self):
        if self.audio_kilo_bitrate is None or self.audio_kilo_bitrate == 0:
            return None
        return str(self.audio_kilo_bitrate) + "k"


__all__ = [
    'Representation'
]
