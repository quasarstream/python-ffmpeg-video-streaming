"""
ffmpeg_streaming.media
~~~~~~~~~~~~

Auto Generate Representation and Representation Object


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
from ._format import Format
from ._media_property import Size, Bitrate

MINIMUM_BITRATE = 65536


class Representation:
    def __init__(self, size: Size, bitrate: Bitrate, **options):
        """
        @TODO: add documentation
        """
        self.size = size
        self.bitrate = bitrate
        self.options = options


def min_bitrate(bitrate: int) -> int:
    """
    @TODO: add documentation
    """
    if bitrate < MINIMUM_BITRATE:
        return MINIMUM_BITRATE

    return bitrate


def reduce_bitrate(bitrate: Bitrate, divide: int) -> Bitrate:
    """
    @TODO: add documentation
    """
    if divide == 1:
        return bitrate

    divide = 1 + divide / 2

    overall = min_bitrate(int(bitrate.overall_ / divide))
    video = min_bitrate(int(bitrate.video_ / divide)) if bitrate.video_ is not None and bitrate.video_ != 0 else None
    audio = min_bitrate(int(bitrate.audio_ / divide)) if bitrate.audio_ is not None and bitrate.audio_ != 0 else None

    return Bitrate(video, audio, overall)


def cal_bitrate(bitrate, org_bitrate: Bitrate, index: int) -> Bitrate:
    return bitrate[index - 1] if bitrate is not None else reduce_bitrate(org_bitrate, index)


class AutoRep(object):
    def __init__(self, original_size: Size, original_bitrate: Bitrate, _format: Format,
                 heights: list = None, bitrate: list = None, include_original: bool = True):
        """
        @TODO: add documentation
        """
        self.include_original = include_original
        self.original_bitrate = original_bitrate
        self.original_size = original_size
        self._format = _format
        self.heights = heights if heights is not None else [2160, 1440, 1080, 720, 480, 360, 240, 144]
        self.bitrate = bitrate
        self.is_default = True if heights is not None and bitrate is not None else False

        if heights is not None and bitrate is not None and len(heights) != len(bitrate):
            raise ValueError("The length of heights list must the same as length of bitrate")

    def __iter__(self):
        """
        @TODO: add documentation
        """
        if not self.is_default:
            height = self.original_size.ratio.calculate_height(self.original_size.width, self._format.multiply())
            original = [height] if self.include_original else []
            self.heights = original + list(filter(lambda x: x < height, self.heights))

        self.index = 0

        return self

    def __next__(self):
        """
        @TODO: add documentation
        """
        if self.index < len(self.heights):
            height = self.heights[self.index]
            width = self.original_size.ratio.calculate_width(height, self._format.multiply())
            self.index += 1

            return Representation(Size(width, height), cal_bitrate(self.bitrate, self.original_bitrate, self.index))
        else:
            raise StopIteration


__all__ = [
    'Representation'
]
