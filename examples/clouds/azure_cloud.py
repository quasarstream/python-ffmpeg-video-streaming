"""
examples.clouds.azure_clod
~~~~~~~~~~~~

Open a file from a Microsoft Azure cloud and save hls files to it


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

from azure.storage.blob import BlockBlobService

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')
start_time = time.time()


class MicrosoftAzure(Clouds):
    def __init__(self, **options):
        self.block_blob_service = BlockBlobService(**options)

    def upload_directory(self, directory, **options):
        container = options.pop('container', None)
        if container is None:
            raise ValueError('You should pass a container name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        try:
            for file in files:
                self.block_blob_service.create_blob_from_path(container, file, join(directory, file))
        except:
            error = "An error occurred while uploading the directory"
            logging.error(error)
            raise RuntimeError(error)

    def download(self, filename=None, **options):
        container = options.pop('container', None)
        blob = options.pop('blob', None)

        if container is None or blob is None:
            raise ValueError('You should pass a container name and a blob name')

        if filename is None:
            with tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False) as tmp:
                filename = tmp.name

        try:
            self.block_blob_service.get_blob_to_path(container, blob, filename)
            logging.info("The " + filename + " file was downloaded")
        except:
            error = "An error occurred while downloading the file"
            logging.error(error)
            raise RuntimeError(error)

        return filename


def azure_cloud(container, blob):
    # see https://docs.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage to get credentials
    cloud = MicrosoftAzure(account_name='account_name', account_key='account_key')

    download_options = {
        'container': container,
        'blob': blob
    }
    upload_options = {
        'container': container,
    }

    from_azure_cloud = (cloud, download_options, None)
    to_azure_cloud = (cloud, upload_options)

    return from_azure_cloud, to_azure_cloud


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

    parser.add_argument('-c', '--container', required=True, help='Bucket name (required).')
    parser.add_argument('-b', '--blob', required=True, help='Key name (required)')

    args = parser.parse_args()

    from_azure_cloud, to_azure_cloud = azure_cloud(args.container, args.blob)

    (
        ffmpeg_streaming
            .hls(from_azure_cloud)
            .format('libx264')
            .auto_rep()
            .package(clouds=to_azure_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
