"""
ffmpeg_streaming.media
~~~~~~~~~~~~

Size and Bitrate Objects


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import math

OVERALL_TO_VIDEO_COEFFICIENT = 1
MAX_RATE_COEFFICIENT = 1.2
BUFFER_SIZE = 65536


def cnv_bitrate(bitrate: int, _type: str) -> str:
    if _type == "k":
        bitrate = round(bitrate / 1024)
    elif _type == "m":
        bitrate = round(bitrate / 1024 * 1024)
    else:
        raise ValueError("Unknown type!")

    return str(bitrate) + _type


class Bitrate:
    def __init__(self, video: int = None, audio: int = None, overall: int = None, **kwargs):
        """
        @TODO: add documentation
        """
        if video is None and overall is None:
            raise ValueError("You must at least specify value of the video or overall format")
        self.overall_ = overall
        self.video_ = video
        self.audio_ = audio
        self.kwargs = kwargs
        self.type = kwargs.pop("type", "k")

    @property
    def overall(self):
        """
        @TODO: add documentation
        """
        return cnv_bitrate(self.overall_, self.type) if self.overall_ is not None else None

    @property
    def video(self):
        """
        @TODO: add documentation
        """
        return cnv_bitrate(self.video_, self.type) if self.video_ is not None else None

    @property
    def audio(self):
        """
        @TODO: add documentation
        """
        return cnv_bitrate(self.audio_, self.type) if self.audio_ is not None else 'copy'

    def calc_video(self, convert: bool = True):
        """
        @TODO: add documentation
        """
        if self.video_ is not None and self.video_ != 0:
            val = self.video_
        else:
            val = int(self.overall_ * OVERALL_TO_VIDEO_COEFFICIENT)

        return cnv_bitrate(val, self.type) if convert else val

    @property
    def calc_overall(self):
        """
        @TODO: add documentation
        """
        return self.overall_ if self.overall_ is not None else self.video_ + self.audio_


def multiple_up(value, multiple):
    while 0 != value % multiple:
        value += 1

    return value


def multiple_down(value, multiple):
    while 0 != value % multiple:
        value -= 1

    return value


class Ratio:
    def __init__(self, width: int, height: int):
        """
        @TODO: add documentation
        """
        self.width = width
        self.height = height

    def get_value(self) -> float:
        return self.width / self.height

    def calculate_width(self, height: int, multiple: int = 1) -> int:
        """
        @TODO: add documentation
        """
        max_w = multiple_up(math.ceil(self.get_value() * height), multiple)
        min_w = multiple_down(math.floor(self.get_value() * height), multiple)

        max_r = abs(self.get_value() - (max_w / height))
        min_r = abs(self.get_value() - (min_w / height))

        return max_w if max_r < min_r else min_w

    def calculate_height(self, width: int, multiple: int = 1) -> int:
        """
        @TODO: add documentation
        """
        max_h = multiple_up(math.ceil(width / self.get_value()), multiple)
        min_h = multiple_down(math.floor(width / self.get_value()), multiple)

        max_r = abs(self.get_value() - (width / max_h))
        min_r = abs(self.get_value() - (width / min_h))

        return max_h if max_r < min_r else min_h


class Size:
    def __init__(self, width: int, height: int):
        """
        @TODO: add documentation
        """
        self.width = width
        self.height = height

    @property
    def ratio(self) -> Ratio:
        """
        @TODO: add documentation
        """
        return Ratio(self.width, self.height)

    def __str__(self) -> str:
        """
        @TODO: add documentation
        """
        return f"{self.width}x{self.height}"


__all__ = [
    'Size',
    'Bitrate'
]