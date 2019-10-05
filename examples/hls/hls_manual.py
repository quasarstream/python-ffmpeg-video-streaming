import argparse
import sys
import ffmpeg_streaming

from ffmpeg_streaming import Representation


def transcode_progress(percentage, ffmpeg, media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')
    parser.add_argument('-o', '--output', default=None, help='The output to write files.')

    args = parser.parse_args()

    rep1 = Representation(width=256, height=144, kilo_bitrate=200, audio_k_bitrate=64)
    rep2 = Representation(width=854, height=480, kilo_bitrate=500, audio_k_bitrate=128)
    rep3 = Representation(width=1080, height=720, kilo_bitrate=1000, audio_k_bitrate=320)

    (
        ffmpeg_streaming
            .hls(args.input, hls_time=10, hls_allow_cache=1)
            .format('libx264')
            .add_rep(rep1, rep2, rep3)
            .package(args.output, transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
