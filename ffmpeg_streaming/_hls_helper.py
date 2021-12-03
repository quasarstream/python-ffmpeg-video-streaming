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

from ffmpeg_streaming._utiles import mkdir, get_path_info


class HLSKeyInfoFile:
    def __init__(self, key_info_file_path: str, path: str, url: str, period: int = 0, needle: str = '', length: int = 16):
        """
        @TODO: add documentation
        """
        self.needle = needle
        self.period = period
        self.segments = []
        self.length = length
        self.url = self.c_url = url
        self.path = self.c_path = path
        mkdir(os.path.dirname(path))
        self.key_info_file_path = key_info_file_path

    def __str__(self):
        """
        @TODO: add documentation
        """
        self.generate()
        return self.key_info_file_path

    def generate(self):
        """
        @TODO: add documentation
        """
        self.generate_key()
        self.update_key_info_file()

    def generate_key(self):
        """
        @TODO: add documentation
        """
        with open(self.path, 'wb') as key:
            key.write(token_bytes(self.length))

    def update_key_info_file(self):
        """
        @TODO: add documentation
        """
        with open(self.key_info_file_path, 'w') as key_info_file:
            key_info_file.write("\n".join([self.url, self.path, token_hex(self.length)]))

    def update_suffix(self):
        """
        @TODO: add documentation
        """
        unique = uuid.uuid4()
        self.path = self.c_path + "-" + str(unique)
        self.url = self.c_url + "-" + str(unique)

    def rotate_key(self, line: str):
        """
        @TODO: add documentation
        """
        if self.needle in line and line not in self.segments:
            self.segments.append(line)
            if len(self.segments) % self.period == 0:
                self.update_suffix()
                self.generate()

def sub_info(rep, sub_path) -> list:
    """
    Returns the subtitle information to be added to manifest.

    Parameters
    ----------
    rep : Representation
    sub_path : subtitle manifest file name
    """
    tag = '#EXT-X-MEDIA:'
    info = [
        f'TYPE=SUBTITLES',
        f'GROUP-ID="subs"',
        f'NAME="subtitles"',
        f'URI="'+sub_path+'"'
    ]
    return [tag + ",".join(info)]

def stream_info(rep, sub_exists) -> list:
    """
    @TODO: add documentation
    """
    tag = '#EXT-X-STREAM-INF:'
    info = [
        f'BANDWIDTH={rep.bitrate.calc_overall}',
        f'RESOLUTION={rep.size}',
        f'NAME="{rep.size.height}"'
    ]
    if sub_exists:
        info.append(f'SUBTITLES="subs"')
    custom = rep.options.pop('stream_info', [])

    return [tag + ",".join(info + custom)]


class HLSMasterPlaylist:
    def __init__(self, media):
        """
        @TODO: add documentation
        """
        self.media = media

    @classmethod
    def generate(cls, media, path=None):
        if path is None:
            path = "{}.m3u8".format(os.path.join(*get_path_info(media.output_)))
        with open(path, 'w', encoding='utf-8') as playlist:
            playlist.write(cls(media)._content())

    def _content(self) -> str:
        """
        @TODO: add documentation
        """
        content = ['#EXTM3U'] + self._get_version() + self.media.options.get('description', [])

        for rep in self.media.reps:
            sub_exists=os.path.isfile(os.path.dirname(self.media.output_)+'/'+self.sub_path(rep)[0])
            if(sub_exists):
                content += sub_info(rep,self.sub_path(rep)[0]) + stream_info(rep,sub_exists) + self.stream_path(rep)
            else:
                content += stream_info(rep,sub_exists) + self.stream_path(rep)

        return "\n".join(content)

    def _get_version(self) -> list:
        """
        @TODO: add documentation
        """
        version = "7" if self.media.options.get('hls_segment_type', '') == 'fmp4' else "3"
        return ['#EXT-X-VERSION:' + version]

    def stream_path(self, rep):
        """
        @TODO: add documentation
        """
        return ["{}_{}p.m3u8".format(os.path.basename(self.media.output_).split('.')[0], rep.size.height)]

    def sub_path(self, rep):
        """
        Returns the subtitles maifest file name.

        Parameters
        ----------
        rep : Representation
        """
        return ["{}_{}p_vtt.m3u8".format(os.path.basename(self.media.output_).split('.')[0], rep.size.height)]
