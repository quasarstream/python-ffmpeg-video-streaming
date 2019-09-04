from pprint import pprint

from ffmpeg_streaming import FFProbe
from .utiles import round_to_even
from .rep import Representation


def get_kilo_bit_rates(kilo_bit_rate, count):
    kilo_bites = []
    divided_by = 1.5

    while count:
        k_bit_rate = int(kilo_bit_rate/divided_by)
        kilo_bites.append(k_bit_rate)
        divided_by += .5
        count -= 1

    return kilo_bites


class AutoRepresentation:
    def __init__(self, ffprobe, heights):
        if not isinstance(ffprobe, FFProbe):
            raise TypeError('The input must be instance of FFProbe')
        self.format = ffprobe.format()
        self.video = ffprobe.streams().video()

        if heights is None:
            heights = [2160, 1080, 720, 480, 360, 240, 144]
        self.heights = heights
        
    def generate(self):
        width, height, ratio = self.dimension()
        kilo_bitrate = self.kilo_bitrate()

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

    def kilo_bitrate(self):
        try:
            return round(int(self.video['bit_rate']) / 1024)
        except KeyError:
            try:
                return round((int(self.format['bit_rate']) / 1024) * .9)
            except KeyError:
                raise KeyError('It could not determine the value of video bitrate')
