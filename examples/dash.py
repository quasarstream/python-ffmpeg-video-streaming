import ffmpeg_streaming


def progress(percentage, line, all_media):
    print("{}% is transcoded".format(percentage))


def create_dash_files():
    (
        ffmpeg_streaming
            .dash('/var/www/media/videos/test.wmv', adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package('/var/www/media/videos/dash/test.mpd', progress)
    )


if __name__ == "__main__":
    create_dash_files()
