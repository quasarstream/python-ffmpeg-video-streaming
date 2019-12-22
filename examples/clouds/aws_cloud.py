"""
examples.clouds.aws_cloud
~~~~~~~~~~~~

Open a file from a Amazon S3 cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import datetime
import logging
import sys
import tempfile
import time
from os import listdir
from os.path import isfile, join

import boto3
import botocore

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


class AWS(Clouds):
    def __init__(self, **options):
        self.s3 = boto3.client('s3', **options)

    def upload_directory(self, directory, **options):
        bucket_name = options.pop('bucket_name', None)
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        for file in files:
            full_path_file = directory + file
            self.s3.upload_file(full_path_file, bucket_name, file)

    def download(self, filename=None, **options):
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
            filename = tmp.name

        bucket_name = options.pop('bucket_name', None)
        key = options.pop('key', None)
        if bucket_name is None or key is None:
            raise ValueError('You should pass a bucket name and a key')

        try:
            self.s3.Bucket(bucket_name).download_file(key, filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise RuntimeError("The object does not exist.")
            else:
                raise RuntimeError("Could not connect to the server")

        return filename


def aws_cloud(bucket_name, key):
    cloud = AWS(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET')
    download_options = {
        'bucket_name': bucket_name,
        'key': key,
    }
    upload_options = {
        'bucket_name': bucket_name,
    }

    from_aws_cloud = (cloud, download_options, None)
    to_aws_cloud = (cloud, upload_options)

    return from_aws_cloud, to_aws_cloud


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
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--bucket_name', required=True, help='Bucket name (required).')
    parser.add_argument('-k', '--key', required=True, help='Key name (required)')

    args = parser.parse_args()

    from_aws_cloud, to_aws_cloud = aws_cloud(args.bucket_name, args.key)

    (
        ffmpeg_streaming
            .dash(from_aws_cloud, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package('/var/www/media/stream.mpd', to_aws_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
