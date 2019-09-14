import os
import sys
import ffmpeg_streaming
from ffmpeg_streaming import Representation


def progress(percentage, line, sec):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Transcoding... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def create_dash_files(_input, _output, __progress=None):
    rep1 = Representation(width=256, height=144, kilo_bitrate=200, audio_k_bitrate=64)
    rep2 = Representation(width=854, height=480, kilo_bitrate=500, audio_k_bitrate=128)
    rep3 = Representation(width=1080, height=720, kilo_bitrate=1000, audio_k_bitrate=320)

    (
        ffmpeg_streaming
            .dash(_input, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .add_rep(rep1, rep2, rep3)
            .package(_output, __progress)
    )


if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    _input = os.path.join(current_dir, '_example.mp4')
    _output = os.path.join(current_dir, name, 'output')

    _progress = progress

    create_dash_files(_input, _output, _progress)
