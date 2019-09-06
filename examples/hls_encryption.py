import ffmpeg_streaming


def progress(percentage, line, all_media):
    print("{}% is transcoded".format(percentage))


def create_encrypted_hls_files():
    (
        ffmpeg_streaming
            .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
            .encryption('aminyazdanpanah.com', 'c:\\test\\amin.enc')
            .format('libx264')
            .auto_rep()
            .package('/var/www/media/videos/hls/test.m3u8', progress)
    )


if __name__ == "__main__":
    create_encrypted_hls_files()
