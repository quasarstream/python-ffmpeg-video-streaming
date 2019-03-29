class Representation:
    def __init__(self, width, height, bitrate):
        self.width = width
        self.height = height
        self.bitrate = bitrate

    def size(self):
        return str(self.width) + "x" + str(self.height)

    def bit_rate(self):
        return str(self.bitrate) + "k"
