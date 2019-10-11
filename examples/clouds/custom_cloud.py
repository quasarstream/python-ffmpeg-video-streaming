"""
examples.clouds.cloud
~~~~~~~~~~~~

Open a file from a custom cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import sys

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


def transcode_progress(percentage, ffmpeg, media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
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
