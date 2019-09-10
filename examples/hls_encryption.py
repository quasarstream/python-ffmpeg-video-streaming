import os
import sys
import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\r Transcoding... (%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def create_encrypted_hls_files(_input, _output, url_to_key, save_to, __progress=None):
    (
        ffmpeg_streaming
            .hls(_input)
            .encryption(url_to_key, save_to)
            .format('libx264')
            .auto_rep()
            .package(_output, __progress)
    )


if __name__ == "__main__":
    create_dir = os.path.basename(__file__).split('.')[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    _input = os.path.join(current_dir, '_example.mp4')
    _output = os.path.join(current_dir, create_dir, 'output')

    # A URL (or a path) to access the key on your website
    # It is highly recommended to protect the key on your website(e.g using a token or check a session/cookie)
    _url_to_key = 'https://www.aminyazdanpanah.com/keys/enc.key'
    # or _url_to_key = '/keys/enc.key'

    # The full pathname of the file where a random key will be created
    # Note: The path of the key should be accessible from your website(e.g. '/var/www/public_html/keys/enc.key')
    _save_to = os.path.join(current_dir, 'enc.key')

    _progress = progress

    create_encrypted_hls_files(_input, _output, _url_to_key, _save_to, _progress)
