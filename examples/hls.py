import sys
import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r %s%% is transcoded [%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
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
    _input = '/var/www/media/videos/test.mkv'
    _output = '/var/www/media/videos/hls/test.m3u8'
    _progress = progress

    create_hls_files(_input, _output, _progress)
