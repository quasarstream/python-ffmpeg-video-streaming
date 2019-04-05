from .utiles import round_to_even
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
    def __init__(self, stream, heights):
        if not isinstance(stream, Streams):
            raise TypeError('The input must be instance of Streams')
        self.video = stream.video()

        if heights is None:
            heights = [2160, 1080, 720, 480, 240, 144]
        self.heights = heights
        
    def generate(self):
        width, height, ratio = self.dimension()
        kilo_bitrate = round(int(self.video['bit_rate']) / 1024)

        reps = [Representation(width=width, height=height, kilo_bitrate=kilo_bitrate)]

        heights = list(filter(lambda x: x < height, self.heights))
        k_bit_rates = get_kilo_bit_rates(kilo_bitrate, len(heights))
        i = 0

        for height in heights:
            reps.append(Representation(width=round_to_even(height*ratio), height=height, kilo_bitrate=k_bit_rates[i]))
            i += 1

        return reps

    def dimension(self):
        width = self.video['width']
        height = self.video['height']
        ratio = width / height

        return width, height, ratio
