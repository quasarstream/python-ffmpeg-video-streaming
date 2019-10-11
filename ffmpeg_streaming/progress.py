"""
ffmpeg_streaming.progress
~~~~~~~~~~~~

Parse realtime FFmpeg lines to gives a percentage of transcoding


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import re

from ffmpeg_streaming.utiles import convert_to_sec


def progress(line, total_sec):
    time = re.search('(?<=time=)\w+:\w+:\w+', line)
    if time:
        sec = convert_to_sec(time.group(0))
        return round(100 * sec / total_sec)


def get_duration_sec(line):
    time = re.search('(?<=Duration: )\w+:\w+:\w+', line)
    if time:
        return convert_to_sec(time.group(0))
