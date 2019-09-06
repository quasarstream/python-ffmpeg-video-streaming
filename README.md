# 📼 Python FFMpeg Video Streaming
This package uses the **[FFmpeg](https://ffmpeg.org)** to package media content for online streaming(DASH and HLS)

**Contents**
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [DASH](#dash)
  - [HLS](#hls)
    - [Encrypted HLS](#encrypted-hls)
  - [Progress](#progress)
  - [Probe](#probe)
- [Several Open Source Players](#several-open-source-players)
- [Contributing and Reporting Bugs](#contributing-and-reporting-bugs)
- [Credits](#credits)
- [License](#license)

## Requirements
1. This version of the package is only compatible with Python 3.0 or higher.

2. To use this package, you need to **[install the FFMpeg](https://ffmpeg.org/download.html)**. You will need both FFMpeg and FFProbe binaries to use it.

## Installation
The latest version of `ffmpeg-streaming` can be acquired via pip:
```
pip install python-ffmpeg-video-streaming
```

## Quickstart
The best way to learn how to use this library is to review the examples and browse the source code as it is self-documented.

### DASH
**[Dynamic Adaptive Streaming over HTTP (DASH)](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)**, also known as MPEG-DASH, is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers.

Similar to Apple's HTTP Live Streaming (HLS) solution, MPEG-DASH works by breaking the content into a sequence of small HTTP-based file segments, each segment containing a short interval of playback time of content that is potentially many hours in duration, such as a movie or the live broadcast of a sports event. The content is made available at a variety of different bit rates, i.e., alternative segments encoded at different bit rates covering aligned short intervals of playback time. While the content is being played back by an MPEG-DASH client, the client uses a bit rate adaptation (ABR) algorithm to automatically select the segment with the highest bit rate possible that can be downloaded in time for playback without causing stalls or re-buffering events in the playback. The current MPEG-DASH reference client dash.js offers both buffer-based (BOLA) and hybrid (DYNAMIC) bit rate adaptation algorithms. Thus, an MPEG-DASH client can seamlessly adapt to changing network conditions and provide high quality playback with fewer stalls or re-buffering events. [Learn more](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)
 
Create DASH Files:
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
You can also create representations manually:
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
See **[DASH options](https://ffmpeg.org/ffmpeg-formats.html#dash-2)** for more information.

### HLS
**[HTTP Live Streaming (also known as HLS)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)** is an HTTP-based adaptive bitrate streaming communications protocol implemented by Apple Inc. as part of its QuickTime, Safari, OS X, and iOS software. Client implementations are also available in Microsoft Edge, Firefox and some versions of Google Chrome. Support is widespread in streaming media servers.

HLS resembles MPEG-DASH in that it works by breaking the overall stream into a sequence of small HTTP-based file downloads, each download loading one short chunk of an overall potentially unbounded transport stream. A list of available streams, encoded at different bit rates, is sent to the client using an extended M3U playlist. [Learn more](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)
 
Create HLS files based on original video(auto generate qualities).
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

You can also create representations manually:
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
**NOTE:** You cannot use HEVC(libx265) and VP9 formats for HLS packaging.

#### Encrypted HLS
The encryption process requires some kind of secret (key) together with an encryption algorithm. HLS uses AES in cipher block chaining (CBC) mode. This means each block is encrypted using the ciphertext of the preceding block. [Learn more](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

You need to pass both `URL to the key` and `path to save a random key` to the `encryption` method:

```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
        .encryption('https://www.aminyazdanpanah.com/keys/enc.key', '/var/www/my_website_project/keys/enc.key')
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8')
)
```
**NOTE:** It is very important to protect your key on your website using a token or a session/cookie(****It is highly recommended****).    

See **[HLS options](https://ffmpeg.org/ffmpeg-formats.html#hls-2)** for more information.

### Progress
You can get realtime information about the transcoding by passing a callable method to the `package` method:
```python
import ffmpeg_streaming

def progress(percentage, line, all_media):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    print("{}% is transcoded".format(percentage))

(
    ffmpeg_streaming
        .hls('/var/www/media/videos/test.mp4', hls_time=10, hls_allow_cache=1)
        .encryption('https://www.aminyazdanpanah.com/keys/enc.key', '/var/www/my_website_project/keys/enc.key')
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8', progress)
)
```
Output:
``` bash
1% is transcoded
2% is transcoded
.
.
.
99% is transcoded
100% is transcoded

Process finished with exit code 0
```

### Probe
You can extract the metadata of video file using the following code:
```python
from pprint import pprint
from ffmpeg_streaming import FFProbe

ffprobe = FFProbe('/var/www/media/test.mp4')
```
**NOTE:** You can save these metadata to your database.

See the [example](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/probe.py) for more information.

## Several Open Source Players
You can use these libraries to play your streams.
- **WEB**
    - DASH and HLS: **[video.js](https://github.com/videojs/video.js)**
    - DASH and HLS: **[DPlayer](https://github.com/MoePlayer/DPlayer)**
    - DASH and HLS: **[Plyr](https://github.com/sampotts/plyr)**
    - DASH and HLS: **[MediaElement.js](https://github.com/mediaelement/mediaelement)**
    - DASH and HLS: **[Clappr](https://github.com/clappr/clappr)**
    - DASH and HLS: **[Flowplayer](https://github.com/flowplayer/flowplayer)**
    - DASH and HLS: **[Shaka Player](https://github.com/google/shaka-player)**
    - DASH and HLS: **[videojs-http-streaming (VHS)](https://github.com/videojs/http-streaming)**
    - DASH: **[dash.js](https://github.com/Dash-Industry-Forum/dash.js)**
    - HLS: **[hls.js](https://github.com/video-dev/hls.js)**
- **Android**
    - DASH and HLS: **[ExoPlayer](https://github.com/google/ExoPlayer)**

**NOTE:** You should pass a manifest of stream(e.g. `https://www.aminyazdanpanah.com/videos/dash/lesson-1/test.mpd` or `/videos/hls/lesson-2/test.m3u8` ) to these players.

## Contributing and Reporting Bugs
I'd love your help in improving, correcting, adding to the specification.
Please **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)** or **[submit a pull request](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls)**.
- Please see **[Contributing File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md)** for more information.
- If you have any questions or you want to report a bug, please just **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)**
- If you discover a security vulnerability within this package, please see **[SECURITY File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/SECURITY.md)** for more information to help with that.

**NOTE:** If you have any questions about this package or FFMpeg, please **DO NOT** send an email to me or submit the contact form on my website. Emails related to these issues **will be ignored**.


## Credits
- **[Amin Yazdanpanah](https://www.aminyazdanpanah.com/?u=github.com/aminyazdanpanah/python-ffmpeg-video-streaming)**

## License
The MIT License (MIT). Please see **[License File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)** for more information.
