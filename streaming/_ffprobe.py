import json
import subprocess
from .streams import Streams


def ffprobe(filename, cmd='ffprobe'):

    args = [cmd, '-show_format', '-show_streams', '-of', 'json', filename]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    return Streams(json.loads(out.decode('utf-8')))


__all__ = [
    'ffprobe',
]
