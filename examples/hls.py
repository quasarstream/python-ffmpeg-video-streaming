from pprint import pprint

import streaming

ffprobe = streaming.ffprobe('c:\\test\\test.mp4')
video = ffprobe.video()

pprint(video)

