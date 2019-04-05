from pprint import pprint

import ffmpeg_streaming

ffprobe = ffmpeg_streaming.ffprobe('c:\\test\\test.mp4')
video = ffprobe.video()

pprint(video)

