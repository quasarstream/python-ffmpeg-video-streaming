import argparse
import sys
import ffmpeg_streaming

from ffmpeg_streaming.from_clouds import from_url


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
    parser = argparse.ArgumentParser()

    parser.add_argument('-url', '--url', required=True, help='The URL to the video file.')
    parser.add_argument('-o', '--output', required=True, help='The output to write files.')

    args = parser.parse_args()

    (
        ffmpeg_streaming
            .hls(from_url(args.url, progress=download_progress), hls_time=20)
            .format('libx264')
            .auto_rep()
            .package(args.output, progress=transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
