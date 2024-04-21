"""
ffmpeg_streaming.process
~~~~~~~~~~~~

Run FFmpeg commands and monitor FFmpeg


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import shlex
import subprocess
import threading
import logging
import time

from ffmpeg_streaming._hls_helper import HLSKeyInfoFile
from ffmpeg_streaming._utiles import get_time, time_left


def _p_open(commands, **options):
    """
    @TODO: add documentation
    """
    logging.info("ffmpeg running command: {}".format(commands))
    return subprocess.Popen(shlex.split(commands), **options)


class Process(object):
    out = None
    err = None

    def __init__(self, media, commands: str, monitor: callable = None, **options):
        """
        @TODO: add documentation
        """
        self.is_monitor = False
        self.input = options.pop('input', None)
        self.timeout = options.pop('timeout', None)
        default_proc_opts = {
            'stdin': None,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
            'universal_newlines': False
        }
        default_proc_opts.update(options)
        options.update(default_proc_opts)
        if callable(monitor) or isinstance(getattr(media, 'key_rotation'), HLSKeyInfoFile):
            self.is_monitor = True
            options.update({
                'stdin': subprocess.PIPE,
                'universal_newlines': True
            })

        self.process = _p_open(commands, **options)
        self.media = media
        self.monitor = monitor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.kill()

    def _monitor(self):
        """
        @TODO: add documentation
        """
        duration = 1
        _time = 0
        log = []
        start_time = time.time()

        while True:
            line = self.process.stdout.readline().strip()
            if line == '' and self.process.poll() is not None:
                break

            if line != '':
                log += [line]

            if isinstance(getattr(self.media, 'key_rotation'), HLSKeyInfoFile):
                getattr(self.media, 'key_rotation').rotate_key(line)

            if callable(self.monitor):
                duration = get_time('Duration: ', line, duration)
                _time = get_time('time=', line, _time)
                self.monitor(line, duration, _time, time_left(start_time, _time, duration), self.process)

        Process.out = log

    def _thread_mon(self):
        """
        @TODO: add documentation
        """
        thread = threading.Thread(target=self._monitor)
        thread.start()

        thread.join(self.timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            error = 'Timeout! exceeded the timeout of {} seconds.'.format(str(self.timeout))
            logging.error(error)
            raise RuntimeError(error)

    def run(self):
        """
        @TODO: add documentation
        """
        if self.is_monitor:
            self._thread_mon()
        else:
            Process.out, Process.err = self.process.communicate(self.input, self.timeout)

        if self.process.poll():
            error = str(Process.err) if Process.err else str(Process.out)
            logging.error('ffmpeg failed to execute command: {}'.format(error))
            raise RuntimeError('ffmpeg failed to execute command: ', error)

        logging.info("ffmpeg executed command successfully")

        return Process.out, Process.err
