"""
examples.clouds.cloud
~~~~~~~~~~~~

Open a file from a cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import datetime
import logging
import socket
import sys
import tempfile
import time
from os import listdir
from os.path import isfile, join

import requests

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


class Cloud(Clouds):
    def upload_directory(self, directory, **options):
        field_name = options.pop('field_name', None)

        if field_name is None:
            raise ValueError('You should specify a field_name')

        method = options.pop('method', 'post')
        url = options.pop('url', None)
        upload_files = []

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in files:
            upload_files.append((field_name, open(join(directory, file), 'rb')))

        r = requests.request(method, url, files=upload_files, **options)

        if not r.ok:
            raise RuntimeError('Error uploading file!')

    def download(self, filename=None, **options):
        progress = options.pop('progress', None)
        method = options.pop('method', 'get')
        url = options.pop('url', None)

        if url is None:
            raise ValueError('You should specify an url')

        if filename is None:
            file = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
        else:
            file = open(filename, 'wb')

        with file as f:
            response = requests.request(method, url, stream=True, **options)
            total_byte = response.headers.get('content-length')

            if total_byte is None or not callable(progress):
                f.write(response.content)
            else:
                downloaded = 0
                total_byte = int(total_byte)
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    percentage = round(100 * downloaded / total_byte)
                    progress(percentage, downloaded, total_byte)
                sys.stdout.write('\n')

            return f.name


def download_progress(percentage, downloaded, total):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rDownloading...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def cloud():
    _cloud = Cloud()
    download_options = {
        'url': 'https://www.aminyazdanpanah.com/my_sweetie.mp4',
        'progress': download_progress
    }
    upload_options = {
        'url': 'https://localhost:8000/api/upload',
        'method': 'post',
        'field_name': 'YOUR_FIELD_NAME',
        'auth': ('username', 'password'),
        'headers': {
            'User-Agent': 'Mozilla/5.0 (compatible; ' + socket.gethostname() + 'Bot/1.0; +' + socket.getfqdn + '/bots)',
            'Accept': 'application/json',
            'Authorization': 'Bearer ACCESS_TOKEN'
        }
    }

    from_cloud = (_cloud, download_options, None)
    to_cloud = (_cloud, upload_options)

    return from_cloud, to_cloud


start_time = time.time()
logging.basicConfig(filename='Transcoding-' + str(start_time) + '.log', level=logging.DEBUG)


def per_to_time_left(percentage):
    if percentage != 0:
        diff_time = time.time() - start_time
        seconds_left = 100 * diff_time / percentage - diff_time
        time_left = str(datetime.timedelta(seconds=int(seconds_left))) + ' left'
    else:
        time_left = 'calculating...'

    return time_left


def transcode_progress(per, ffmpeg):
    # You can update a field in your database or can log it to a file
    # You can also create a socket connection and show a progress bar to users
    logging.debug(ffmpeg)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    from_cloud, to_cloud = cloud()

    (
        ffmpeg_streaming
            .dash(from_cloud, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package('/var/www/media/stream.mpd', to_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
