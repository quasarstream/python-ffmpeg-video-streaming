class Representation:
    def __init__(self, **kwargs):
        self.width = kwargs.pop('width', None)
        self.height = kwargs.pop('height', None)
        self.bitrate = kwargs.pop('bitrate', None)

    def size(self):
        if self.width is None or self.height is None:
            raise ValueError("You must set the width and the height of video")
        return str(self.width) + "x" + str(self.height)

    def bit_rate(self):
        if self.bitrate is None:
            raise ValueError("You must set the bitrate of video")
        return str(self.bitrate) + "k"


__all__ = [
    'Representation'
]
