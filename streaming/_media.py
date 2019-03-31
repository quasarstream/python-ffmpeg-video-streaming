from .hls import HLS
from .dash import DASH


def dash(filename, **kwargs):
    return DASH(filename, kwargs)


def hls(filename):
    return HLS(filename)


__all__ = [
    'dash',
    'hls',
]
