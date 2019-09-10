import os
import sys
import ffmpeg_streaming


def progress(percentage, line, all_media):
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
    create_dir = os.path.basename(__file__).split('.')[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    _input = os.path.join(current_dir, '_example.mp4')
    _output = os.path.join(current_dir, create_dir, 'output')

    _progress = progress

    create_hls_files(_input, _output, _progress)
