import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep1 = Representation(width=256, height=144, kilo_bitrate=200)
rep2 = Representation(width=426, height=240, kilo_bitrate=500)
rep3 = Representation(width=640, height=360, kilo_bitrate=1000)

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .add_rep(rep1, rep2, rep3)
        .package('/var/www/media/videos/hls/test.m3u8')
)


