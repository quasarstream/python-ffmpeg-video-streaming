import importlib.metadata

from ._clouds import *
from ._format import *
from ._input import *
from ._media_property import *
from ._reperesentation import *
from .ffprobe import *

try:
    __version__: str = importlib.metadata.version("python-ffmpeg-video-streaming")
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = None


__all__ = ["__version__"] + _input.__all__ + _format.__all__ + _reperesentation.__all__ + _media_property.__all__ + _clouds.__all__ + ffprobe.__all__
