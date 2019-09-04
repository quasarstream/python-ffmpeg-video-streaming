from pprint import pprint
from ffmpeg_streaming import FFProbe

ffprobe = FFProbe('/var/www/media/test.mp4')

ffprobe.save_as_json('/var/www/media/test_metadata.json')

video_format = ffprobe.format()
videos = ffprobe.streams().videos()
audios = ffprobe.streams().audios()
first_video = ffprobe.streams().video()
first_audio = ffprobe.streams().audio()

print("format:\n")
pprint(video_format)

print("\nvideos:\n")
for video in videos:
    pprint(video)

print("\naudios:\n")
for audio in audios:
    pprint(audio)

print("\nfirst video:\n")
pprint(first_video)

print("\nfirst audio\n")
pprint(first_audio)



