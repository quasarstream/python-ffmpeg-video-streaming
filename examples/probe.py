from pprint import pprint
from ffmpeg_streaming import FFProbe


def ffprobe():
    return FFProbe('/var/www/media/test.mp4')


if __name__ == "__main__":
    ffprobe = ffprobe()

    ffprobe.save_as_json('/var/www/media/test_metadata.json')

    all_media = ffprobe.all()

    video_format = ffprobe.format()

    streams = ffprobe.streams().all()
    videos = ffprobe.streams().videos()
    audios = ffprobe.streams().audios()

    first_stream = ffprobe.streams().first_stream()
    first_video = ffprobe.streams().video()
    first_audio = ffprobe.streams().audio()

    print("all:\n")
    pprint(all_media)

    print("format:\n")
    pprint(video_format)

    print("streams:\n")
    pprint(streams)

    print("\nvideos:\n")
    for video in videos:
        pprint(video)

    print("\naudios:\n")
    for audio in audios:
        pprint(audio)

    print("\nfirst stream:\n")
    pprint(first_stream)

    print("\nfirst video:\n")
    pprint(first_video)

    print("\nfirst audio\n")
    pprint(first_audio)



