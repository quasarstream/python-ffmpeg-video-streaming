import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show the progress to users
    print("{}% is transcoded".format(percentage))


def create_hls_files(_input, _output, __progress=None):
    (
        ffmpeg_streaming
            .hls(_input, hls_time=10, hls_allow_cache=1)
            .format('libx264')
            .auto_rep()
            .package(_output, __progress)
    )


if __name__ == "__main__":
    _input = '/var/www/media/videos/test.mkv'
    _output = '/var/www/media/videos/dash/test.mpd'
    _progress = progress

    create_hls_files(_input, _output, _progress)
