from pprint import pprint

from .streams import Streams
from .rep import Representation


def get_kilo_bit_rates(kilo_bit_rate, count):
    kilo_bites = []
    while count:
        kilo_bit_rate = int(kilo_bit_rate/1.3)
        kilo_bites.append(kilo_bit_rate)
        count -= 1
    return kilo_bites


class AutoRepresentation:
    def __init__(self, ffprob):
        self.heights = [2160, 1080, 720, 480, 240, 144]
        if not isinstance(ffprob, Streams):
            raise TypeError('The input must be instance of Streams')
        self.video = ffprob.video()

    def generate(self):
        width, height, ratio = self.dimension()
        less_than_height = list(filter(lambda x: x < height, self.heights))
        kilo_bit_rate = round(int(self.video['bit_rate']) / 1024)
        reps = [Representation(width=width, height=height, bitrate=kilo_bit_rate)]
        kilo_bit_rates = get_kilo_bit_rates(kilo_bit_rate, len(less_than_height))
        count = 0
        for height in less_than_height:
            reps.append(Representation(width=int(height*ratio), height=height, bitrate=kilo_bit_rates[count]))
            count += 1

        return reps

    def dimension(self):
        width = self.video['width']
        height = self.video['height']
        ratio = width / height

        return width, height, ratio

