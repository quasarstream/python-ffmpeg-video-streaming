class Streams:
    def __init__(self, stream):
        self.stream = stream

    def is_video(self):
        video = next((stream for stream in self.stream['streams'] if stream['codec_type'] == 'video'), None)
        if video is None:
            raise ValueError('No video stream found')
        return video

    def is_audio(self):
        audio = next((stream for stream in self.stream['streams'] if stream['codec_type'] == 'audio'), None)
        if audio is None:
            raise ValueError('No audio stream found')
        return audio

    def first(self):
        return self.stream['streams'][0]
