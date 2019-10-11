"""
examples.clouds.cloud
~~~~~~~~~~~~

Open a file from a cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import sys

import ffmpeg_streaming
from ffmpeg_streaming import Cloud


def download_progress(percentage, downloaded, total):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rDownloading...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def transcode_progress(percentage, ffmpeg, media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def main():
    cloud = Cloud()
    download_options = {
        'url': 'https://www.aminyazdanpanah.com/my_sweetie.mp4',
        'progress': download_progress
    }
    upload_options = {
        'url': 'https://localhost:8000/api/upload',
        'method': 'post',
        'auth': ('username', 'password'),
        'headers': {
            'User-Agent': 'Mozilla/5.0 (compatible; AminYazdanpanahBot/1.0; +http://aminyazdanpanah.com/bots)',
            'Accept': 'application/json',
            'Authorization': 'Bearer ACCESS_TOKEN'
        }
    }

    from_cloud = (cloud, download_options, None)
    to_cloud = (cloud, upload_options)

    (
        ffmpeg_streaming
            .dash(from_cloud, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package('/var/www/media/stream.mpd', to_cloud, transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
