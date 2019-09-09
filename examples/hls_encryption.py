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
    _input = '/var/www/media/videos/test.3gp'
    _output = '/var/www/media/videos/hls/test.m3u8'

    # A URL (or a path) to access the key on your website
    # It is highly recommended to protect the key on your website(e.g using a token or check a session/cookie)
    _url_to_key = 'https://www.aminyazdanpanah.com/keys/enc.key'
    # or _url_to_key = '/keys/enc.key'

    # The full pathname of the file where a random key will be created
    # Please note that the path of the key should be accessible from your website
    _save_to = '/var/www/public_html/keys/enc.key'

    _progress = progress

    create_encrypted_hls_files(_input, _output, _url_to_key, _save_to, _progress)
