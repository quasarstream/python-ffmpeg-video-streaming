class Streams:
    def __init__(self, streams):
        self.streams = streams

    def video(self):
        return self.get_stream('video')

    def audio(self):
        return self.get_stream('audio')

    def first_stream(self):
        return self.streams[0]

    def videos(self):
        return self.get_streams('video')

    def audios(self):
        return self.get_streams('audio')

    def get_stream(self, media):
        media_attr = next((stream for stream in self.streams if stream['codec_type'] == media), None)
        if media_attr is None:
            raise ValueError('No ' + str(media) + ' stream found')
        return media_attr

    def get_streams(self, media):
        for stream in self.streams:
            if stream['codec_type'] == media:
                yield stream
