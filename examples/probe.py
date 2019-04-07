from pprint import pprint

import ffmpeg_streaming

ffprobe = ffmpeg_streaming.ffprobe('/path/to/the/file')
video = ffprobe.video()

pprint(video)

