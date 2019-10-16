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
import sys

import ffmpeg_streaming
from ffmpeg_streaming import GoogleCloudStorage


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


def transcode_progress(percentage, ffmpeg):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
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
