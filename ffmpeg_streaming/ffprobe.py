"""
ffmpeg_streaming._ffprobe
~~~~~~~~~~~~

Probe the video


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import json
import logging
import subprocess

from ._media_property import Size, Bitrate


class Streams:
    def __init__(self, streams):
        self.streams = streams

    def video(self, ignore_error=True):
        """
        @TODO: add documentation
        """
        return self._get_stream('video', ignore_error)

    def audio(self, ignore_error=True):
        """
        @TODO: add documentation
        """
        return self._get_stream('audio', ignore_error)

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

    def _get_stream(self, media, ignore_error):
        """
        @TODO: add documentation
        """
        media_attr = next((stream for stream in self.streams if stream['codec_type'] == media), None)
        if media_attr is None and not ignore_error:
            raise ValueError('No {} stream found'.format(str(media)))
        return media_attr if media_attr is not None else {}

    def _get_streams(self, media):
        """
        @TODO: add documentation
        """
        for stream in self.streams:
            if stream['codec_type'] == media:
                yield stream


class FFProbe:
    def __init__(self, filename, cmd='ffprobe'):
        """
        @TODO: add documentation
        """
        commands = [cmd, '-show_format', '-show_streams', '-of', 'json', filename]
        logging.info("ffprobe running command: {}".format(" ".join(commands)))
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.out, err = process.communicate()
        if process.returncode != 0:
            logging.error(str(self.out) + str(err))
            raise RuntimeError('ffprobe', self.out, err)
        logging.info("ffprobe executed command successfully!")

    def streams(self):
        """
        @TODO: add documentation
        """
        return Streams(json.loads(self.out.decode('utf-8'))['streams'])

    def format(self):
        """
        @TODO: add documentation
        """
        return json.loads(self.out.decode('utf-8'))['format']

    def all(self):
        """
        @TODO: add documentation
        """
        return json.loads(self.out.decode('utf-8'))

    def save_as_json(self, path):
        """
        @TODO: add documentation
        """
        with open(path, 'w') as probe:
            probe.write(self.out.decode('utf-8'))

    @property
    def video_size(self) -> Size:
        """
        @TODO: add documentation
        """
        width = int(self.streams().video().get('width', 0))
        height = int(self.streams().video().get('height', 0))

        if width == 0 or height == 0:
            raise RuntimeError('It could not determine the value of width/height')

        return Size(width, height)

    @property
    def bitrate(self, _type: str = "k") -> Bitrate:
        """
        @TODO: add documentation
        """
        overall = int(self.format().get('bit_rate', 0))
        video = int(self.streams().video().get('bit_rate', 0))
        audio = int(self.streams().audio().get('bit_rate', 0))

        if overall == 0:
            raise RuntimeError('It could not determine the value of bitrate')

        return Bitrate(video, audio, overall, type=_type)


__all__ = [
    'FFProbe'
]
