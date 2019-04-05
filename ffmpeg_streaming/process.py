import subprocess
import ffmpeg_streaming
from .params import (get_hls_parm, get_dash_parm)


def build_command(cmd, media_obj):
    if type(cmd) != list:
        cmd = [cmd]

    cmd += ['-y', '-i', media_obj.filename]
    cmd += ['-c:v', media_obj.format]

    if isinstance(media_obj, ffmpeg_streaming.HLS):
        cmd += get_hls_parm(media_obj)
    elif isinstance(media_obj, ffmpeg_streaming.DASH):
        cmd += get_dash_parm(media_obj)
    # print(cmd)
    # exit()
    return cmd


def run_async(media, cmd='ffmpeg', pipe_stdin=False, pipe_stdout=False, pipe_stderr=False):
    commands = build_command(cmd, media)
    stdin_stream = subprocess.PIPE if pipe_stdin else None
    stdout_stream = subprocess.PIPE if pipe_stdout else None
    stderr_stream = subprocess.PIPE if pipe_stderr else None
    return subprocess.Popen(commands, stdin=stdin_stream, stdout=stdout_stream, stderr=stderr_stream)


def run(media, cmd='ffmpeg', capture_stdout=False, capture_stderr=False, input=None):
    process = run_async(
        media,
        cmd,
        pipe_stdin=input is not None,
        pipe_stdout=capture_stdout,
        pipe_stderr=capture_stderr,
    )
    out, err = process.communicate(input)
    retcode = process.poll()
    if retcode:
        raise RuntimeError('ffmpeg', out, err)
    return out, err
