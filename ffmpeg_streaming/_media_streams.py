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
        """
        @TODO: add documentation
        """
        return self._get_stream('video')

    def audio(self):
        """
        @TODO: add documentation
        """
        return self._get_stream('audio')

    def first_stream(self):
        """
        @TODO: add documentation
        """
        return self.streams[0]

    def all(self):
        """
        @TODO: add documentation
        """
        return self.streams

    def videos(self):
        """
        @TODO: add documentation
        """
        return self._get_streams('video')

    def audios(self):
        """
        @TODO: add documentation
        """
        return self._get_streams('audio')

    def _get_stream(self, media):
        """
        @TODO: add documentation
        """
        media_attr = next((stream for stream in self.streams if stream['codec_type'] == media), None)
        if media_attr is None:
            raise ValueError('No ' + str(media) + ' stream found')
        return media_attr

    def _get_streams(self, media):
        """
        @TODO: add documentation
        """
        for stream in self.streams:
            if stream['codec_type'] == media:
                yield stream
