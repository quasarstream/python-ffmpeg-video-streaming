"""
ffmpeg_streaming.streams
~~~~~~~~~~~~

Parse streams that is the output of the FFProbe


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""


class Streams:
    def __init__(self, streams):
        self.streams = streams

    def video(self):
        return self._get_stream('video')

    def audio(self):
        return self._get_stream('audio')

    def first_stream(self):
        return self.streams[0]

    def all(self):
        return self.streams

    def videos(self):
        return self._get_streams('video')

    def audios(self):
        return self._get_streams('audio')

    def _get_stream(self, media):
        media_attr = next((stream for stream in self.streams if stream['codec_type'] == media), None)
        if media_attr is None:
            raise ValueError('No ' + str(media) + ' stream found')
        return media_attr

    def _get_streams(self, media):
        for stream in self.streams:
            if stream['codec_type'] == media:
                yield stream
