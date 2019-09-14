import shlex
import subprocess
from .progress import progress, get_duration_sec
from .utiles import clear_tmp_file
from .params import get_hls_parm, get_dash_parm


def build_command(cmd, media_obj):
    if type(cmd) != list:
        cmd = [cmd]

    cmd += ['-y', '-i', media_obj.filename.replace("\\", "/")]
    cmd += ['-c:v', media_obj.video_format]

    if media_obj.audio_format is not None:
        cmd += ['-c:a', media_obj.audio_format]

    media_name = type(media_obj).__name__

    if media_name == 'HLS':
        cmd += get_hls_parm(media_obj)
    elif media_name == 'DASH':
        cmd += get_dash_parm(media_obj)

    return " ".join(cmd)


def run_async(media, cmd='ffmpeg', pipe_stdin=False, pipe_stdout=False, pipe_stderr=True, universal_newlines=False):
    commands = build_command(cmd, media)
    stdin_stream = subprocess.PIPE if pipe_stdin else None
    stdout_stream = subprocess.PIPE if pipe_stdout else None
    stderr_stream = subprocess.STDOUT if pipe_stderr else False
    return subprocess.Popen(shlex.split(commands), stdout=stdout_stream, stderr=stderr_stream, stdin=stdin_stream
                            , universal_newlines=universal_newlines)


def clear_tmp_files(media):
    clear_tmp_file(media.filename)
    if media.__class__.__name__ == 'HLS':
        clear_tmp_file(media.hls_key_info_file)


def show_progress(media, callable_progress, cmd, input):
    process = run_async(
        media,
        cmd,
        pipe_stdin=input is not None,
        pipe_stdout=True,
        pipe_stderr=True,
        universal_newlines=True
    )

    total_sec = None
    log = []

    while True:
        line = process.stdout.readline().strip()
        log += [line]

        if line == '' and process.poll() is not None:
            break

        if total_sec is None:
            total_sec = get_duration_sec(line)
        else:
            percentage = progress(line, total_sec)
            if percentage is not None:
                callable_progress(percentage, line, total_sec)

    clear_tmp_files(media)
    if process.poll():
        raise RuntimeError('ffmpeg', " ".join(log))

    return media, log


def run(media, callable_progress=None, cmd='ffmpeg', capture_stdout=False, capture_stderr=True,
        input=None, timeout=None):

    if callable(callable_progress):
        return show_progress(media, callable_progress, cmd, input)

    process = run_async(
        media,
        cmd,
        pipe_stdin=input is not None,
        pipe_stdout=capture_stdout,
        pipe_stderr=capture_stderr,
    )
    out, err = process.communicate(input, timeout=timeout)

    clear_tmp_files(media)

    if process.poll():
        raise RuntimeError('ffmpeg', out, err)
    return media, [out, err]
