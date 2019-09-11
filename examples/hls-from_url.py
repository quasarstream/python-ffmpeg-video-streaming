import os
import sys
import ffmpeg_streaming
from ffmpeg_streaming.from_clouds import from_url


def download_progress(percentage, downloaded, total):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Downloading... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def progress(percentage, line, sec):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Transcoding... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def create_hls_files(_input, _output, __progress=None):
    (
        ffmpeg_streaming
            .hls(_input, hls_time=20)
            .format('libx264')
            .auto_rep()
            .package(_output, __progress)
    )


if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    url = 'https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/_example.mp4?raw=true'
    _input = from_url(url, progress=download_progress)
    _output = os.path.join(current_dir, name, 'output')

    _progress = progress

    create_hls_files(_input, _output, _progress)
