# Python FFMpeg Video Streaming
This library uses the [FFmpeg](https://ffmpeg.org) to package media content for online streaming(DASH and HLS)

## Installation

The latest version of `ffmpeg-streaming` can be acquired via pip:

```
pip install python-ffmpeg-video-streaming
```


## Documentation

The best way to learn how to use this library is to review the examples and browse the source code as it is self-documented.

### Required Libraries

This library requires a working FFMpeg and FFProbe binaries to use it.

For installing the FFmpeg and also the FFprobe, just Google "install ffmpeg on" + `your operation system`


### DASH
**[Dynamic Adaptive Streaming over HTTP (DASH)](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)**, also known as MPEG-DASH, is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers.


#### Auto Create DASH Files
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .dash('/var/www/media/videos/test.mp4', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package('/var/www/media/videos/dash/test.mpd')
)
```


#### Create Representations Manually
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep1 = Representation(width=256, height=144, kilo_bitrate=200)
rep2 = Representation(width=426, height=240, kilo_bitrate=500)
rep3 = Representation(width=640, height=360, kilo_bitrate=1000)

(
    ffmpeg_streaming
        .dash('/var/www/media/videos/test.mp4', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .add_rep(rep1, rep2, rep3)
        .package('/var/www/media/videos/dash/test.mpd')
)

```

For more information about [FFMpeg](https://ffmpeg.org/) and its dash options, [see here](https://ffmpeg.org/ffmpeg-formats.html#dash-2).
### HLS

**[HTTP Live Streaming (also known as HLS)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)** is an HTTP-based media streaming communications protocol implemented by [Apple Inc](https://www.apple.com/).

```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8')
)
```

#### Create Representations Manually
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep1 = Representation(width=256, height=144, kilo_bitrate=200)
rep2 = Representation(width=426, height=240, kilo_bitrate=500)
rep3 = Representation(width=640, height=360, kilo_bitrate=1000)

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .add_rep(rep1, rep2, rep3)
        .package('/var/www/media/videos/hls/test.m3u8')
)
```
For more information about which value you should pass to these methods and also HLS options, [see here](https://ffmpeg.org/ffmpeg-formats.html#hls-2).

#### Encryption HLS

The encryption process requires some kind of secret (key) together with an encryption algorithm.

HLS uses AES in cipher block chaining (CBC) mode. This means each block is encrypted using the cipher text of the preceding block. [read more](http://hlsbook.net/how-to-encrypt-hls-video-with-ffmpeg/)

Before we can encrypt our videos, we need an encryption key. I’m going to use OpenSSL to create the key, which we can do like so:

``` bash 
openssl rand 16 > enc.key
```

The next step is to generate an IV. This step is optional. (If no value is provided, the segment sequence number will be used instead.)
``` bash
openssl rand -hex 16
ecd0d06eaf884d8226c33928e87efa33
```

Make a note of the output as you’ll need it shortly.

To encrypt the video we need to tell ffmpeg what encryption key to use, the URI of the key, and so on. We use `setHlsKeyInfoFile` method and passing the location of a key info file. The file must be in the following format:

``` bash
Key URI
Path to key file
IV (optional)
```

The first line specifies the URI of the key, which will be written to the playlist. The second line is the path to the file containing the encryption key, and the (optional) third line contains the initialisation vector. Here’s an example (enc.keyinfo):

``` bash
https://example.com/enc.key
enc.key
ecd0d06eaf884d8226c33928e87efa33
```

Now that we have everything we need, run the following code to encrypt the video segments:

```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1, hls_key_info_file="/path/to/keyinfo")
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8')
)
```

Reference: http://hlsbook.net/

## Contributing

I'd love your help in improving, correcting, adding to the specification.
Please [file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)
or [submit a pull request](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls).

Please see [Contributing File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md) for more information.

## Security

If you discover a security vulnerability within this package, please send an e-mail to Amin Yazdanpanah via:

contact [AT] aminyazdanpanah • com.
## Credits

- [Amin Yazdanpanah](http://www.aminyazdanpanah.com/?u=github.com/aminyazdanpanah/python-ffmpeg-video-streaming)

## License

The MIT License (MIT). Please see [License File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE) for more information.
