from .media import (HLS, DASH)


def dash(filename, **kwargs):
    return DASH(filename, kwargs)


def hls(filename):
    return HLS(filename)


__all__ = [
    'dash',
    'hls',
]
