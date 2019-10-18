"""
examples.clouds.azure_clod
~~~~~~~~~~~~

Open a file from a Microsoft Azure cloud and save hls files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import datetime
import sys
import time

import ffmpeg_streaming
from ffmpeg_streaming import MicrosoftAzure


def azure_cloud(container, blob):
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
