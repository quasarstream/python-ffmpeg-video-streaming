import os

from ffmpeg_streaming import FFProbe


def ffprobe(__input):
    return FFProbe(__input)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    _input = os.path.join(current_dir, '_example.mp4')

    ffprobe = ffprobe(_input)

    ffprobe.save_as_json(os.path.join(current_dir, 'probe.json'))

    all_media = ffprobe.all()

    video_format = ffprobe.format()

    streams = ffprobe.streams().all()
    videos = ffprobe.streams().videos()
    audios = ffprobe.streams().audios()

    first_stream = ffprobe.streams().first_stream()
    first_video = ffprobe.streams().video()
    first_audio = ffprobe.streams().audio()

    print("all:")
    print(all_media)

    print("format:")
    print(video_format)

    print("streams:")
    print(streams)

    print("videos:")
    for video in videos:
        print(video)

    print("audios:")
    for audio in audios:
        print(audio)

    print("first stream:")
    print(first_stream)

    print("first video:")
    print(first_video)

    print("first audio:")
    print(first_audio)



