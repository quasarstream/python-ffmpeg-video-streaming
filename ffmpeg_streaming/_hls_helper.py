"""
ffmpeg_streaming.media
~~~~~~~~~~~~

HLS helper


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import os
import uuid
from secrets import token_bytes, token_hex

from ffmpeg_streaming._utiles import mkdir


class HLSKeyInfoFile:
    def __init__(self, key_info_file_path: str, path: str, url: str, period: int = 0, needle: str = '', length: int = 16):
        self.needle = needle
        self.period = period
        self.segments = []
        self.length = length
        self.url = self.c_url = url
        self.path = self.c_path = path
        mkdir(os.path.dirname(path))
        self.key_info_file_path = key_info_file_path

    def __str__(self):
        self.generate()
        return self.key_info_file_path

    def generate(self):
        self.generate_key()
        self.update_key_info_file()

    def generate_key(self):
        with open(self.path, 'wb') as key:
            key.write(token_bytes(self.length))

    def update_key_info_file(self):
        with open(self.key_info_file_path, 'w') as key_info_file:
            key_info_file.write("\n".join([self.url, self.path, token_hex(self.length)]))

    def update_suffix(self):
        unique = uuid.uuid4()
        self.path = self.c_path + "-" + str(unique)
        self.url = self.c_url + "-" + str(unique)

    def rotate_key(self, line: str):
        if self.needle in line and line not in self.segments:
            self.segments.append(line)
            if len(self.segments) % self.period == 0:
                self.update_suffix()
                self.generate()


def stream_info(rep) -> list:
    # @TODO: add custom stream info
    tag = '#EXT-X-STREAM-INF:'
    info = [
        'BANDWIDTH=' + str(rep.bitrate.normalize_video(False)),
        'RESOLUTION=' + rep.size.normalize,
        'NAME="' + str(rep.size.height) + '"'
    ]
    
    return [tag + ",".join(info)]


class HLSMasterPlaylist:
    def __init__(self, media):
        self.media = media
        self.path = media.output

    @classmethod
    def generate(cls, media):
        path = os.path.join(os.path.dirname(media.output_), os.path.basename(media.output_).split('.')[0] + '.m3u8')
        with open(path, 'w', encoding='utf-8') as playlist:
            playlist.write(cls(media)._content())

    def _content(self) -> str:
        content = ['#EXTM3U'] + self._get_version() + self.media.options.get('description', [])

        for rep in self.media.reps:
            content += stream_info(rep) + self.stream_path(rep)

        return "\n".join(content)

    def _get_version(self) -> list:
        version = "7" if hasattr(self.media, 'fragmented_mp4') else "3"
        return ['#EXT-X-VERSION:' + version]

    def stream_path(self, rep):
        return [str(os.path.basename(self.media.output_).split('.')[0]) + "_" + str(rep.size.height) + "p.m3u8"]
