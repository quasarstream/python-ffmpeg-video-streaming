class Representation:
    def __init__(self, **kwargs):
        self.width = kwargs.pop('width', None)
        self.height = kwargs.pop('height', None)
        self.kilo_bitrate = kwargs.pop('kilo_bitrate', None)

    @property
    def size(self):
        if self.width is None or self.height is None:
            raise ValueError("You must set the width and the height of video")
        return str(self.width) + "x" + str(self.height)

    @property
    def bit_rate(self):
        if self.kilo_bitrate is None:
            raise ValueError("You must set the bitrate of video")
        return str(self.kilo_bitrate) + "k"


__all__ = [
    'Representation'
]
