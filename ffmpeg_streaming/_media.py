from .media import (HLS, DASH)


def dash(filename, **kwargs):
    return DASH(filename, kwargs)


def hls(filename, **kwargs):
    return HLS(filename, kwargs)


__all__ = [
    'dash',
    'hls',
]
