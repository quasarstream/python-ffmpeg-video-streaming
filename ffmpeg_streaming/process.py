import shlex
import subprocess
from .progress import progress, get_duration_sec
from .utiles import clear_tmp_file
from .args import get_hls_args, get_dash_args


def build_command(cmd, media_obj):
    if type(cmd) != list:
        cmd = [cmd]

    cmd += ['-y', '-i', '"' + media_obj.filename.replace("\\", "/") + '"']
    cmd += ['-c:v', media_obj.video_format]

    if media_obj.audio_format is not None:
        cmd += ['-c:a', media_obj.audio_format]

    media_name = type(media_obj).__name__

    if media_name == 'HLS':
        cmd += get_hls_args(media_obj)
    elif media_name == 'DASH':
        cmd += get_dash_args(media_obj)

    return " ".join(cmd)


def run_async(media, cmd='ffmpeg', pipe_stdin=False, pipe_stdout=False, pipe_stderr=subprocess.STDOUT,
              universal_newlines=False):

    commands = build_command(cmd, media)
    stdin_stream = subprocess.PIPE if pipe_stdin else None
    stdout_stream = subprocess.PIPE if pipe_stdout else None
    stderr_stream = pipe_stderr

    return subprocess.Popen(shlex.split(commands), stdout=stdout_stream, stderr=stderr_stream, stdin=stdin_stream
                            , universal_newlines=universal_newlines)


def clear_tmp_files(media):
    clear_tmp_file(media.filename)
    if media.__class__.__name__ == 'HLS':
        clear_tmp_file(media.hls_key_info_file)


def show_progress(media, callable_progress, cmd, c_stdin):
    process = run_async(
        media,
        cmd,
        pipe_stdin=c_stdin,
        pipe_stdout=True,
        pipe_stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    total_sec = None
    log = []
    percentage = 0

    while True:
        line = process.stdout.readline().strip()

        if line != '':
            log += [line]

        if line == '' and process.poll() is not None:
            break

        if total_sec is None:
            total_sec = get_duration_sec(line)
        else:
            c_percentage = progress(line, total_sec)
            if c_percentage is not None:
                percentage = c_percentage

        callable_progress(percentage, line, media)

    clear_tmp_files(media)

    if process.poll():
        raise RuntimeError('ffmpeg', " ".join(log[-3:]), " ".join(log))

    return media, log


def run(media, c_progress=None, cmd='ffmpeg', c_stdout=False, c_stderr=True, c_stdin=False, c_input=None, timeout=None):
    if callable(c_progress):
        return show_progress(media, c_progress, cmd, c_stdin)

    process = run_async(
        media,
        cmd,
        pipe_stdin=c_stdin,
        pipe_stdout=c_stdout,
        pipe_stderr=subprocess.PIPE if c_stderr else False,
    )
    out, err = process.communicate(c_input, timeout=timeout)

    clear_tmp_files(media)

    if process.poll():
        raise RuntimeError('ffmpeg', err, out)
    return media, [out, err]
