from .hls import HLS
from .dash import DASH


def dash(filename):
    return DASH(filename)


def hls(filename):
    return HLS(filename)


__all__ = [
    'dash',
    'hls',
]
