import json
import subprocess


def probe(filename, cmd='ffprobe'):

    args = [cmd, '-show_format', '-show_streams', '-of', 'json', filename]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    return json.loads(out.decode('utf-8'))


__all__ = [
    'probe',
]