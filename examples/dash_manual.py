import ffmpeg_streaming
from ffmpeg_streaming import Representation


def progress(percentage, line, all_media):
    print("{}% is transcoded".format(percentage))


def create_dash_files():
    rep1 = Representation(width=256, height=144, kilo_bitrate=200)
    rep2 = Representation(width=426, height=240, kilo_bitrate=500)
    rep3 = Representation(width=640, height=360, kilo_bitrate=1000)

    (
        ffmpeg_streaming
            .dash('/var/www/media/videos/test.avi', adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .add_rep(rep1, rep2, rep3)
            .package('/var/www/media/videos/dash/test.mpd', progress)
    )


if __name__ == "__main__":
    create_dash_files()
