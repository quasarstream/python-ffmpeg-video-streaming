"""
examples.clouds.google_cloud
~~~~~~~~~~~~

Open a file from a google cloud and save hls files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import datetime
import sys
import tempfile
import time
from os import listdir
from os.path import isfile, join

from google.cloud import storage

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


class GoogleCloudStorage(Clouds):
    def __init__(self, bucket_name, **kwargs):
        storage_client = storage.Client(**kwargs)
        self.bucket_name = bucket_name
        self.bucket = storage_client.get_bucket(bucket_name)

    def upload_directory(self, directory, **options):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in files:
            full_path_file = directory + file
            blob = self.bucket.blob(self.bucket_name + file, options)
            blob.upload_from_filename(full_path_file)

    def download(self, filename=None, **options):
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
            filename = tmp.name

        object_name = options.pop('object_name', None)
        if object_name is None:
            raise ValueError('You should pass an object name')

        blob = self.bucket.get_blob(object_name, options)
        blob.download_to_filename(filename)

        return filename


def google_cloud(bucket_name, object_name):
    cloud = GoogleCloudStorage(bucket_name)
    download_options = {
        'object_name': object_name,
    }
    upload_options = {
        'encryption': 'SOME_BASE64_ENCRYPTION',
    }

    from_google_cloud = (cloud, download_options, None)
    to_google_cloud = (cloud, upload_options)

    return from_google_cloud, to_google_cloud


start_time = time.time()


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
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--bucket_name', required=True, help='Bucket name (required).')
    parser.add_argument('-o', '--object_name', required=True, help='object name (required).')

    args = parser.parse_args()

    from_google_cloud, to_google_cloud = google_cloud(args.bucket_name, args.object_name)

    (
        ffmpeg_streaming
            .hls(from_google_cloud)
            .format('libx264')
            .auto_rep()
            .package('/var/www/media/stream.mpd', to_google_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
