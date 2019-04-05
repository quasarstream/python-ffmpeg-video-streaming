import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep1 = Representation(width=640, height=360, kilo_bitrate=190)
rep2 = Representation(width=625, height=853, kilo_bitrate=200)
rep3 = Representation(width=152, height=365, kilo_bitrate=630)
reps = (
    ffmpeg_streaming
        .dash('c:\\test\\test.mp4', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package('c:\\test\\amin\\mina.mpd')
)

print(reps)
# for rep in reps:
#     print(rep.size(), rep.bit_rate())

