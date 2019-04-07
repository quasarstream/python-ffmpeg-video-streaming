import ffmpeg_streaming

(
    ffmpeg_streaming
        .dash('/var/www/media/videos/test.mp4', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package('/var/www/media/videos/dash/test.mpd')
)



