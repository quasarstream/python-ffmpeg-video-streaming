import os
import sys
import ffmpeg_streaming
from ffmpeg_streaming.from_clouds import from_url


def download_progress(percentage, downloaded, total):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Downloading... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def progress(percentage, ffmpeg, media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Transcoding... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def create_dash_files(_input, _output, __progress=None):
    (
        ffmpeg_streaming
            .dash(_input, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package(_output, __progress)
    )


if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_30mb.mp4'
    _input = from_url(url, progress=download_progress)
    _output = os.path.join(current_dir, name, 'output')

    _progress = progress

    create_dash_files(_input, _output, _progress)
