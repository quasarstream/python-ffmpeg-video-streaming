"""
examples.clouds.cloud
~~~~~~~~~~~~

Open a file from a custom cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import datetime
import logging
import sys
import time

import ffmpeg_streaming
from ffmpeg_streaming import Clouds


class CustomCloud(Clouds):

    def upload_directory(self, directory, **options):
        # @TODO: upload a directory to a cloud
        pass

    def download(self, filename=None, **options):
        # @TODO: download a file to a local path
        pass


def custom_cloud():

    cloud = CustomCloud()
    download_options = {
        'YOUR_OPTIONS': 'my_sweetie.mp4',
    }
    upload_options = {
        'YOUR_OPTIONS': 'my_sweetie.mp4',
    }

    from_custom_cloud = (cloud, download_options, None)
    to_custom_cloud = (cloud, upload_options)

    return from_custom_cloud, to_custom_cloud


logging.basicConfig(filename='streaming.log', level=logging.NOTSET, format='[%(asctime)s] %(levelname)s: %(message)s')
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
    # You can update a field in your database or log it to a file
    # You can also create a socket connection and show a progress bar to users
    logging.info(ffmpeg)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()


def main():
    from_custom_cloud, to_custom_cloud = custom_cloud()

    (
        ffmpeg_streaming
            .dash(from_custom_cloud, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package(clouds=to_custom_cloud, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
