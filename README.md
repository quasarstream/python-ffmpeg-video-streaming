# 📼 Python FFmpeg Video Streaming
[![Build Status](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming.svg?branch=master)](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Build status](https://ci.appveyor.com/api/projects/status/qy712tou5pvq629y?svg=true)](https://ci.appveyor.com/project/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Downloads](https://pepy.tech/badge/python-ffmpeg-video-streaming)](https://pepy.tech/project/python-ffmpeg-video-streaming)
[![PyPI version](https://badge.fury.io/py/python-ffmpeg-video-streaming.svg)](https://badge.fury.io/py/python-ffmpeg-video-streaming)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)

## Overview
This package uses the **[FFmpeg](https://ffmpeg.org)** to package media content for online streaming such as DASH and HLS. You can also use **[DRM](https://en.wikipedia.org/wiki/Digital_rights_management)** for HLS packaging. There are several options to open a file from clouds and save files to them as well.

**Contents**
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Opening a File](#opening-a-file)
  - [DASH](#dash)
  - [HLS](#hls)
    - [Encrypted HLS](#encrypted-hls)
  - [Progress](#progress)
  - [Saving Files](#saving-files)
  - [Probe](#probe)
- [Several Open Source Players](#several-open-source-players)
- [Contributing and Reporting Bugs](#contributing-and-reporting-bugs)
- [Credits](#credits)
- [License](#license)

## Requirements
1. This version of the package is only compatible with **[Python 3.6](https://www.python.org/downloads/)** or higher.

2. To use this package, you need to **[install the FFMpeg](https://ffmpeg.org/download.html)**. You will need both FFMpeg and FFProbe binaries to use it.

## Installation
The latest version of `ffmpeg-streaming` can be acquired via pip:
```
pip install python-ffmpeg-video-streaming
```

## Quickstart
The best way to learn how to use this library is to review ****[the examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples)**** and browse the source code.

### opening a file
There are two ways to open a file:
#### 1. From a Local Path
```python
video = '/var/www/media/videos/test.mp4'
```

#### 2. From Clouds
You can open a file from a cloud by passing a tuple of cloud configuration to the method. There are some options to open a file from **[Amazon Web Services (AWS)](https://aws.amazon.com/)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud. 

```python
video = (google_cloud, download_options, None)
```

Please visit **[this page](https://video.aminyazdanpanah.com/python/start/open-clouds)** to see more examples and usage of these clouds.

### DASH
**[Dynamic Adaptive Streaming over HTTP (DASH)](https://dashif.org/)**, also known as MPEG-DASH, is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers.

Similar to Apple's HTTP Live Streaming (HLS) solution, MPEG-DASH works by breaking the content into a sequence of small HTTP-based file segments, each segment containing a short interval of playback time of content that is potentially many hours in duration, such as a movie or the live broadcast of a sports event. The content is made available at a variety of different bit rates, i.e., alternative segments encoded at different bit rates covering aligned short intervals of playback time. While the content is being played back by an MPEG-DASH client, the client uses a bit rate adaptation (ABR) algorithm to automatically select the segment with the highest bit rate possible that can be downloaded in time for playback without causing stalls or re-buffering events in the playback. The current MPEG-DASH reference client dash.js offers both buffer-based (BOLA) and hybrid (DYNAMIC) bit rate adaptation algorithms. Thus, an MPEG-DASH client can seamlessly adapt to changing network conditions and provide high quality playback with fewer stalls or re-buffering events. [Learn more](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)
 
Create DASH Files:
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .dash(video, adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package('/var/www/media/videos/dash/dash-stream.mpd')
)
```
You can also create representations manually:
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep_144 = Representation(width=256, height=144, kilo_bitrate=95)
rep_240 = Representation(width=426, height=240, kilo_bitrate=150)
rep_360 = Representation(width=640, height=360, kilo_bitrate=276)
rep_480 = Representation(width=854, height=480, kilo_bitrate=750)
rep_720 = Representation(width=1280, height=720, kilo_bitrate=2048)
rep_1080 = Representation(width=1920, height=1080, kilo_bitrate=4096)
rep_1440 = Representation(width=2560, height=1440, kilo_bitrate=6096)

(
    ffmpeg_streaming
        .dash(video, adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .add_rep(rep_144, rep_240, rep_360, rep_480, rep_720, rep_1080, rep_1440)
        .package('/var/www/media/videos/dash/test.mpd')
)

```
See **[DASH examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples/dash)** for more information.

See also **[DASH options](https://ffmpeg.org/ffmpeg-formats.html#dash-2)** for more information about options.

### HLS
**[HTTP Live Streaming (also known as HLS)](https://developer.apple.com/streaming/)** is an HTTP-based adaptive bitrate streaming communications protocol implemented by Apple Inc. as part of its QuickTime, Safari, OS X, and iOS software. Client implementations are also available in Microsoft Edge, Firefox and some versions of Google Chrome. Support is widespread in streaming media servers.

HLS resembles MPEG-DASH in that it works by breaking the overall stream into a sequence of small HTTP-based file downloads, each download loading one short chunk of an overall potentially unbounded transport stream. A list of available streams, encoded at different bit rates, is sent to the client using an extended M3U playlist. [Learn more](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)
 
Create HLS files based on original video(auto generate qualities).
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8')
)
```

You can also create representations manually:
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

rep_360 = Representation(width=640, height=360, kilo_bitrate=276)
rep_480 = Representation(width=854, height=480, kilo_bitrate=750)
rep_720 = Representation(width=1280, height=720, kilo_bitrate=2048)

(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .add_rep(rep_360, rep_480, rep_720)
        .package('/var/www/media/videos/hls/test.m3u8')
)
```
**NOTE:** You cannot use HEVC(libx265) and VP9 formats for HLS packaging.

#### Encrypted HLS
The encryption process requires some kind of secret (key) together with an encryption algorithm. HLS uses AES in cipher block chaining (CBC) mode. This means each block is encrypted using the ciphertext of the preceding block. [Learn more](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

You need to pass both `URL to the key` and `a path to save a random key on your local machine` to the `encryption` method:

```python
import ffmpeg_streaming
(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .encryption('https://www.aminyazdanpanah.com/keys/enc.key', '/var/www/my_website_project/keys/enc.key')
        .format('libx264')
        .auto_rep(heights=[480, 360, 240])
        .package('/var/www/media/videos/hls/test.m3u8')
)
```
**NOTE:** It is very important to protect your key on your website using a token or a session/cookie(****It is highly recommended****).    
See **[HLS examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples/hls)** for more information.

See also **[HLS options](https://ffmpeg.org/ffmpeg-formats.html#hls-2)** for more information about options.

### Progress
You can get realtime information about transcoding by passing callable methods to the `package`:
```python
import sys
import ffmpeg_streaming

def progress(percentage, ffmpeg):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8', progress=progress)
)
```
Output of the progress:
![progress](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/docs/progress.gif?raw=true "progress" )

### Saving Files
There are several options to save your files.

#### 1. To a Local Path
You can pass a local path to the `package` method. If there was no directory in the path, then the package auto makes the directory.
```python
(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/test.m3u8', progress=progress)
)
```
It can also be null. The default path to save files is the input path.
```python
(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package(progress=progress)
)
```
**NOTE:** If you open a file from cloud and did not pass a path to save a file, you will have to pass a local path to the `package` method.

#### 2. To Clouds
You can save your files to clouds by passing a array of cloud configuration to the `package` method. There are some options to save files to **[Amazon Web Services (AWS)](https://aws.amazon.com/)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud. 

```python
(
    ffmpeg_streaming
        .dash('/var/www/media/video.mkv', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package(clouds=[to_aws_cloud, to_azure_cloud, to_google_cloud],
                 progress=progress)
)
``` 
A path can also be passed to save a copy of files on your local machine.
```python
(
    ffmpeg_streaming
        .dash('/var/www/media/video.mkv', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .package(output='/var/www/media/stream.mpd', clouds=[to_aws_cloud, to_google_cloud],
                 progress=progress)
)
```

Please visit **[this page](https://video.aminyazdanpanah.com/python/start/save-clouds)** to see more examples and usage of these clouds.

**NOTE:** You can open a file from your local machine(or a cloud) and save files to a local path or a cloud(or multiple clouds) or both.   

<p align="center"><img src="https://github.com/aminyazdanpanah/aminyazdanpanah.github.io/blob/master/video-streaming/video-streaming.gif?raw=true" width="100%"></p>

### Probe
You can extract the metadata of video file using the following code:
```python
from ffmpeg_streaming import FFProbe

ffprobe = FFProbe('/var/www/media/test.mp4')
```
**NOTE:** You can save these metadata to your database.

See the **[example](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/probe.py)** for more information.

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
- **Windows, Linux, and macOS**
    - DASH and HLS: **[VLC media player](https://github.com/videolan/vlc)**
 

**NOTE:** You should pass a manifest of stream(e.g. `https://www.aminyazdanpanah.com/videos/dash/lesson-1/test.mpd` or `/videos/hls/lesson-2/test.m3u8` ) to these players.

## Contributing and Reporting Bugs
I'd love your help in improving, correcting, adding to the specification.
Please **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)** or **[submit a pull request](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls)**.
- Please see **[Contributing File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md)** for more information.
- If you have any questions or you want to report a bug, please just **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)**
- If you discover a security vulnerability within this package, please see **[SECURITY File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/SECURITY.md)** for more information.

**NOTE:** If you have any questions about this package or FFmpeg, please **DO NOT** send an email to me (or submit the contact form on my website). Emails regarding these issues **will be ignored**.

## Credits
- **[Amin Yazdanpanah](https://www.aminyazdanpanah.com/?u=github.com/aminyazdanpanah/python-ffmpeg-video-streaming)**

## License
The MIT License (MIT). Please see **[License File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)** for more information.
