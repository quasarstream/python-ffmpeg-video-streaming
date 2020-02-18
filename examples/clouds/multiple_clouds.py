"""
examples.clouds.google_cloud
~~~~~~~~~~~~

Open a file from a local path and save dash files to multiple clouds


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import datetime
import logging
import sys
import time

import ffmpeg_streaming
from examples.clouds.aws_cloud import aws_cloud
from examples.clouds.azure_cloud import azure_cloud
from examples.clouds.google_cloud import google_cloud


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
    # logging.info(ffmpeg)
    sys.stdout.write("\rTranscoding...(%s%%) %s [%s%s]" % (per, per_to_time_left(per), '#' * per, '-' * (100 - per)))
    sys.stdout.flush()

def main():
    from_aws_cloud, to_aws_cloud = aws_cloud('bucket_name', 'key')
    from_azure_cloud, to_azure_cloud = azure_cloud('container', 'blob')
    from_google_cloud, to_google_cloud = google_cloud('bucket_name', 'object_name')

    (
        ffmpeg_streaming
            .dash('/var/www/media/video.mkv', adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package(output='/var/www/media/stream.mpd', clouds=[to_aws_cloud, to_azure_cloud, to_google_cloud],
                     progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
