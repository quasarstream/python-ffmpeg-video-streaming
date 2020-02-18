"""
examples.clouds.aws_cloud
~~~~~~~~~~~~

Open a file from a Amazon S3 cloud and save hls files to it


:copyright: (c) 2020 by Amin Yazdanpanah.
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
from botocore.exceptions import ClientError

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')
start_time = time.time()


class AWS(Clouds):
    def __init__(self, **options):
        self.s3 = boto3.client('s3', **options)

    def upload_directory(self, directory, **options):
        bucket_name = options.pop('bucket_name', None)
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        try:
            for file in files:
                self.s3.upload_file(join(directory, file), bucket_name, file)
        except ClientError as e:
            logging.error(e)
            raise RuntimeError(e)

        logging.info("The " + directory + "directory was uploaded to Amazon S3 successfully")

    def download(self, filename=None, **options):
        bucket_name = options.pop('bucket_name', None)
        key = options.pop('key', None)

        if bucket_name is None or key is None:
            raise ValueError('You should pass a bucket name and a key')

        if filename is None:
            filename = tempfile.NamedTemporaryFile(suffix='_' + key + '_py_ff_vi_st.tmp', delete=False)
        else:
            filename = open(filename, 'wb')

        try:
            with filename as f:
                self.s3.download_fileobj(bucket_name, key, f)
            logging.info("The " + filename.name + " file was downloaded")
        except ClientError as e:
            logging.error(e)
            raise RuntimeError(e)

        return filename.name


def aws_cloud(bucket_name, key):
    # see https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html for getting Security Credentials
    cloud = AWS(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET', region_name='YOUR_REGION')
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


def per_to_time_left(percentage):
    if percentage != 0:
        diff_time = time.time() - start_time
        seconds_left = 100 * diff_time / percentage - diff_time
        time_left = str(datetime.timedelta(seconds=int(seconds_left))) + ' left'
    else:
        time_left = 'calculating...'

    return time_left


def transcode_progress(per, ffmpeg):
    # You can update a field in your database or log it to a file
    # You can also create a socket connection and show a progress bar to users
    # logging.info(ffmpeg)
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
            .hls(from_aws_cloud)
            .format('libx264')
            .auto_rep()
            .package(clouds=to_aws_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
