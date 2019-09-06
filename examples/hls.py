import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show the progress to users
    print("{}% is transcoded".format(percentage))


def create_hls_files():
    (
        ffmpeg_streaming
            .hls('/var/www/media/videos/test.mkv', hls_time=10, hls_allow_cache=1)
            .format('libx264')
            .auto_rep()
            .package('/var/www/media/videos/hls/test.m3u8', progress)
    )


if __name__ == "__main__":
    create_hls_files()
