import ffmpeg_streaming


def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show the progress to users
    print("{}% is transcoded".format(percentage))


def create_encrypted_hls_files(_input, _output, url_to_key, save_to, __progress=None):
    (
        ffmpeg_streaming
            .hls(_input, hls_time=10, hls_allow_cache=1)
            .encryption(url_to_key, save_to)
            .format('libx264')
            .auto_rep()
            .package(_output, __progress)
    )


if __name__ == "__main__":
    _input = '/var/www/media/videos/test.3gp'
    _output = '/var/www/media/videos/dash/test.mpd'

    # A URL (or a path) to access the key on your website
    _url_to_key = 'https://www.aminyazdanpanah.com/keys/enc.key'
    # or _url_to_key = '/keys/enc.key'

    # A path you want to save a random key on your local machine
    _save_to = '/var/www/my_website_project/keys/enc.key'

    _progress = progress

    create_encrypted_hls_files(_input, _output, _url_to_key, _save_to, _progress)
