import sys
import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r %s%% is transcoded [%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
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
    _input = '/var/www/media/videos/test.wmv'
    _output = '/var/www/media/videos/dash/test.mpd'
    _progress = progress

    create_dash_files(_input, _output, _progress)
