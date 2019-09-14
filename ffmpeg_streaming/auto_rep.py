from ffmpeg_streaming import FFProbe
from .utiles import round_to_even
from .rep import Representation


def get_kilo_bit_rates(kilo_bit_rate, count):
    kilo_bites = []
    divided_by = 1.5

    while count:
        k_bit_rate = int(kilo_bit_rate/divided_by)
        if k_bit_rate < 64:
            k_bit_rate = 64
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
        self.audio = ffprobe.streams().audio()

        if heights is None:
            heights = [2160, 1080, 720, 480, 360, 240, 144]
        self.heights = heights
        
    def generate(self):
        width, height, ratio = self.dimension()
        video_bitrate, audio_bitrate = self.kilo_bitrate()

        reps = [Representation(width=width, height=height, kilo_bitrate=video_bitrate, audio_k_bitrate=audio_bitrate)]

        heights = list(filter(lambda x: x < height, self.heights))
        v_b_r = get_kilo_bit_rates(video_bitrate, len(heights))
        a_b_r = get_kilo_bit_rates(audio_bitrate, len(heights))
        i = 0

        for height in heights:
            reps.append(Representation(width=round_to_even(height*ratio), height=height, kilo_bitrate=v_b_r[i]
                                       , audio_k_bitrate=a_b_r[i]))
            i += 1

        return reps

    def dimension(self):
        width = self.video.get('width', 0)
        height = self.video.get('height', 0)
        ratio = width / height

        return width, height, ratio

    def kilo_bitrate(self):
        overall_k_bitrate = round((int(self.format.get('bit_rate', 0)) / 1024) * .9)
        video_k_bitrate = round(int(self.video.get('bit_rate', 0)) / 1024)
        audio_k_bitrate = round(int(self.audio.get('bit_rate', 0)) / 1024)

        if video_k_bitrate != 0:
            return video_k_bitrate, audio_k_bitrate
        elif overall_k_bitrate != 0:
            return overall_k_bitrate, audio_k_bitrate
        else:
            raise ValueError('It could not determine the value of video bitrate')
