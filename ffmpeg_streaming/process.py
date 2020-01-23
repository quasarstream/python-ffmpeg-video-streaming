"""
ffmpeg_streaming.process
~~~~~~~~~~~~

Run FFmpeg commands and monitor FFmpeg


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import shlex
import subprocess
import threading
import logging

from .progress import progress, get_duration_sec


def _p_open(commands, p_stdin=False, p_stdout=False, p_stderr=subprocess.STDOUT, universal_newlines=False):

    stdin_stream = subprocess.PIPE if p_stdin else None
    stdout_stream = subprocess.PIPE if p_stdout else None
    stderr_stream = p_stderr
    logging.info("ffmpeg running command: {}".format(commands))

    return subprocess.Popen(shlex.split(commands), stdout=stdout_stream, stderr=stderr_stream, stdin=stdin_stream
                            , universal_newlines=universal_newlines)


class Process(object):
    out = None
    err = None

    def __init__(self, c_progress, commands, c_stdout, c_stderr, c_stdin):
        self.c_progress = c_progress

        if callable(c_progress):
            self.p = _p_open(commands, c_stdin, True, universal_newlines=True)
        else:
            self.p = _p_open(commands, c_stdin, c_stdout, subprocess.PIPE if c_stderr else False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.p.kill()

    def _show_progress(self):
        total_sec = None
        log = []
        percentage = 0

        while True:
            line = self.p.stdout.readline().strip()

            if line != '':
                log += [line]

            if line == '' and self.p.poll() is not None:
                break

            if total_sec is None:
                total_sec = get_duration_sec(line)
            else:
                c_percentage = progress(line, total_sec)
                if c_percentage is not None:
                    percentage = c_percentage

            self.c_progress(percentage, line)

        Process.out = log

    def _thread_progress(self, timeout):
        thread = threading.Thread(target=self._show_progress)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.p.terminate()
            thread.join()
            error = 'Timeout! exceeded the timeout of {} seconds.'.format(str(timeout))
            logging.error(error)
            raise RuntimeError(error)

    def run(self, c_input=None, timeout=None):

        if callable(self.c_progress):
            self._thread_progress(timeout)
        else:
            Process.out, Process.err = self.p.communicate(c_input, timeout=timeout)

        if self.p.poll():
            error = str(Process.err) if Process.err else str(Process.out)
            logging.error('ffmpeg failed to execute command: {}'.format(error))
            raise RuntimeError('ffmpeg failed to execute command: ', error)

        logging.info("ffmpeg executed command successfully")

        return Process.out, Process.err
