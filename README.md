# 📼 Python FFmpeg Video Streaming
[![Build Status](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming.svg?branch=master)](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Build status](https://ci.appveyor.com/api/projects/status/qy712tou5pvq629y?svg=true)](https://ci.appveyor.com/project/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aminyazdanpanah/python-ffmpeg-video-streaming/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aminyazdanpanah/python-ffmpeg-video-streaming/?branch=master)
[![Downloads](https://pepy.tech/badge/python-ffmpeg-video-streaming)](https://pepy.tech/project/python-ffmpeg-video-streaming)
[![PyPI version](https://badge.fury.io/py/python-ffmpeg-video-streaming.svg)](https://badge.fury.io/py/python-ffmpeg-video-streaming)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)

## Overview
This package uses the **[FFmpeg](https://ffmpeg.org)** to package media content for online streaming such as DASH and HLS. You can also use **[DRM](https://en.wikipedia.org/wiki/Digital_rights_management)** for HLS packaging. There are several options to open a file from clouds and save files to them as well.

- The best way to learn how to use this library is to review ****[the examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples)**** and browse the source code.
- For using clouds such as **[Amazon S3](https://aws.amazon.com/s3)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud, please visit **[this page](https://video.aminyazdanpanah.com/python/start/clouds)**.

**Contents**
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Opening a Resource](#opening-a-resource)
  - [DASH](#dash)
  - [HLS](#hls)
    - [DRM (Encrypted HLS)](#drm-encrypted-hls)
  - [Progress](#progress)
  - [Saving Files](#saving-files)
  - [Probe](#probe)
  - [Live](#live)
  - [Conversion](#conversion)
- [Several Open Source Players](#several-open-source-players)
- [Contributing and Reporting Bugs](#contributing-and-reporting-bugs)
- [Credits](#credits)
- [License](#license)

## Requirements
1. This version of the package is only compatible with **[Python 3.6](https://www.python.org/downloads/)** or higher.

2. To use this package, you need to **[install the FFmpeg](https://ffmpeg.org/download.html)**. You will need both FFMpeg and FFProbe binaries to use it.

## Installation
The latest version of `ffmpeg-streaming` can be acquired via pip:
```
pip install python-ffmpeg-video-streaming
```

## Quickstart

### Opening a Resource
There are two ways to open a file:

#### 1. From a FFmpeg supported resource
You can pass a local path of video(or a supported resource) to the method(`hls` or `dash`):
```python
video = '/var/www/media/videos/video.mp4'
```

Please see **[FFmpeg Protocols Documentation](https://ffmpeg.org/ffmpeg-protocols.html)** for more information about supported resources such as `http`, `ftp`, `pipe`, `rtmp` and etc. 

**For example:** 
```python
video = 'https://www.aminyazdanpanah.com/PATH/TO/VIDEO.MP4'
```

#### 2. From Clouds
You can open a file from a cloud by passing a tuple of cloud configuration to the method. 

In **[this page](https://video.aminyazdanpanah.com/python/start/clouds?r=open)**, you will find some examples of opening a file from **[Amazon S3](https://aws.amazon.com/s3)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud. 
```python
video = (google_cloud, download_options, None)
```

### DASH
**[Dynamic Adaptive Streaming over HTTP (DASH)](http://dashif.org/)**, also known as MPEG-DASH, is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers. [Learn more](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)
 
Create DASH files:
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
Generate representations manually:
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

r_144p  = Representation(width=256, height=144, kilo_bitrate=95)
r_240p  = Representation(width=426, height=240, kilo_bitrate=150)
r_360p  = Representation(width=640, height=360, kilo_bitrate=276)
r_480p  = Representation(width=854, height=480, kilo_bitrate=750)
r_720p  = Representation(width=1280, height=720, kilo_bitrate=2048)
r_1080p = Representation(width=1920, height=1080, kilo_bitrate=4096)
r_2k    = Representation(width=2560, height=1440, kilo_bitrate=6144)
r_4k    = Representation(width=3840, height=2160, kilo_bitrate=17408)

(
    ffmpeg_streaming
        .dash(video, adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .add_rep(r_144p, r_240p, r_360p, r_480p, r_720p, r_1080p, r_2k, r_4k)
        .package('/var/www/media/videos/dash/dash-stream.mpd')
)

```
See **[DASH examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples/dash)** and **[DASH options](https://ffmpeg.org/ffmpeg-formats.html#dash-2)** for more information.

### HLS
**[HTTP Live Streaming (also known as HLS)](https://developer.apple.com/streaming/)** is an HTTP-based adaptive bitrate streaming communications protocol implemented by Apple Inc. as part of its QuickTime, Safari, OS X, and iOS software. Client implementations are also available in Microsoft Edge, Firefox and some versions of Google Chrome. Support is widespread in streaming media servers. [Learn more](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)
 
Create HLS files:
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/hls-stream.m3u8')
)
```

Generate representations manually:
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

r_360p = Representation(width=640, height=360, kilo_bitrate=276)
r_480p = Representation(width=854, height=480, kilo_bitrate=750)
r_720p = Representation(width=1280, height=720, kilo_bitrate=2048)

(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .format('libx264')
        .add_rep(r_360p, r_480p, r_720p)
        .package('/var/www/media/videos/hls/hls-stream.m3u8')
)
```
**NOTE:** You cannot use HEVC(libx265) and VP9 formats for HLS packaging.

#### DRM (Encrypted HLS)
The encryption process requires some kind of secret (key) together with an encryption algorithm. HLS uses AES in cipher block chaining (CBC) mode. This means each block is encrypted using the ciphertext of the preceding block. [Learn more](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

You must specify a path to save a random key to your local machine and also a URL(or a path) to access the key on your website(the key you will save must be accessible from your website). You must pass both these parameters to the `encryption` method:

##### Single Key
The following code generates a key for all TS files in a stream.

```python
import ffmpeg_streaming

#A path you want to save a random key to your server
save_to = '/home/public_html/PATH_TO_KEY_DIRECTORY/random_key.key'

#A URL (or a path) to access the key on your website
url = 'https://www.aminyazdanpanah.com/PATH_TO_KEY_DIRECTORY/random_key.key'
# or url = '/PATH_TO_KEY_DIRECTORY/random_key.key'

(
    ffmpeg_streaming
        .hls(video, hls_time=10, hls_allow_cache=1)
        .encryption(url, save_to)
        .format('libx264')
        .auto_rep(heights=[480, 360, 240])
        .package('/var/www/media/videos/hls/hls-stream.m3u8')
)
```

##### Key Rotation
This technique allows you to encrypt each TS file with a new encryption key. This can improve security and allows for more flexibility. You can also use a different key for each set of segments(e.g. if 10 TS files have been generated then rotate the key) or you can generate a new encryption key at every periodic time(e.g. every 10 seconds).
```python
import tempfile
from os.path import join
from random import randrange

import ffmpeg_streaming
from ffmpeg_streaming.key_info_file import generate_key_info_file

save_to = '/home/public_html/PATH_TO_KEY_DIRECTORY/key_rotation'
url = 'https://www.aminyazdanpanah.com/PATH_TO_KEY_DIRECTORY/key_rotation'
key_info_file_path = join(tempfile.gettempdir(), str(randrange(1000, 100000)) + '_py_ff_vi_st.tmp')
k_num = 1

def k_format(name, num):
    return str(name) + "_" + str(num)

def progress(per, ffmpeg):
    global k_num
    if ".ts' for writing" in ffmpeg:
        # A new TS file has been created!
        generate_key_info_file(k_format(url, k_num), k_format(save_to, k_num), key_info_path=key_info_file_path)
        k_num += 1

(
    ffmpeg_streaming
        .hls(video, hls_flags="periodic_rekey")
        .encryption(url, save_to, key_info_path=key_info_file_path)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/hls-stream.m3u8', progress=progress)
)
```
**NOTE:** It is very important to protect your key(s) on your website using a token or a session/cookie(****It is highly recommended****).    

**NOTE:** However HLS supports AES encryption, which you can encrypt your streams, it is not a full DRM solution. If you want to use a full DRM solution, I recommend trying **[FairPlay Streaming](https://developer.apple.com/streaming/fps/)** solution which then securely exchange keys, and protect playback on devices.

See **[HLS examples](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/master/examples/hls)** and **[HLS options](https://ffmpeg.org/ffmpeg-formats.html#hls-2)** for more information.

### Progress
You can get realtime information about transcoding by passing a callable method to the `package` method:
```python
import sys
import ffmpeg_streaming


def progress(percentage, ffmpeg):
    # You can update a field in your database or you can log it to a file(e.x. logging.debug(ffmpeg))
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/hls-stream.m3u8', progress=progress)
)
```
##### Output From a Terminal:
![transcoding](https://github.com/aminyazdanpanah/aminyazdanpanah.github.io/blob/master/video-streaming/transcoding.gif?raw=true "transcoding" )

#### Show a progress bar using **[tqdm](https://github.com/tqdm/tqdm)** 
```python
import ffmpeg_streaming
from tqdm import tqdm

# initialize the tqdm object
bar = tqdm(total=100)
last_per = 0

def progress(percentage, ffmpeg):
    # update the progress bar
    global last_per
    if last_per != percentage:
        bar.update(percentage - last_per)
        last_per = percentage


(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/hls-stream.m3u8', progress=progress)
)

# close the progress bar
bar.close()
```
**NOTE:** Please see **[tqdm documentation](https://github.com/tqdm/tqdm)** for more information.

### Saving Files
There are two ways to save your files.

#### 1. To a Local Path
You can pass a local path to the `package` method. If there was no directory in the path, then the package auto makes the directory.
```python
(
    ffmpeg_streaming
        .hls(video)
        .format('libx264')
        .auto_rep()
        .package('/var/www/media/videos/hls/hls-stream.m3u8', progress=progress)
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
**NOTE:** If you open a file from a cloud and do not pass a path to save the file to your local machine, you will have to pass a local path to the `package` method.

#### 2. To Clouds
You can save your files to a cloud by passing a tuple of cloud configuration to the `package` method. 

In **[this page](https://video.aminyazdanpanah.com/python/start/clouds?r=save)**, you will find some examples of saving files to **[Amazon S3](https://aws.amazon.com/s3)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud. 

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
A path can also be passed to save a copy of files to your local machine.
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
**NOTE:** This option(Save To Clouds) is only valid for **[VOD](https://en.wikipedia.org/wiki/Video_on_demand)** (it does not support live streaming).

**Schema:** The relation is `one-to-many`.

<p align="center"><img src="https://github.com/aminyazdanpanah/aminyazdanpanah.github.io/blob/master/video-streaming/video-streaming.gif?raw=true" width="100%"></p>

### Probe
You can extract the metadata of the video file using the following code:
```python
from ffmpeg_streaming import FFProbe

ffprobe = FFProbe('/var/www/media/video.mp4')
```
**NOTE:** You can save these metadata to your database.

See the **[example](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/probe.py)** for more information.

### Live
You can pass a url(or a supported resource like `ftp`) to live method to upload all the segments files to the HTTP server(or other protocols) using the HTTP PUT method, and update the manifest files every refresh times.

If you want to save stream files to your local machine, please use the `package` method.

```python
# DASH live
import ffmpeg_streaming

(
    ffmpeg_streaming
        .dash('/var/www/media/video.avi', adaption='"id=0,streams=v id=1,streams=a"')
        .format('libx265')
        .auto_rep()
        .live('http://YOUR-WEBSITE.COM/live-stream/out.mpd', progress=progress)
)

# HLS live
(
    ffmpeg_streaming
        .hls('/var/www/media/video.mp4', master_playlist_path='/var/www/stream/live-master-manifest.m3u8')
        .format('libx264')
        .auto_rep()
        .live('http://YOUR-WEBSITE.COM/live-stream/out.m3u8', progress=progress)
)
```
**NOTE:** In the HLS method, you must upload the master manifest to the server manually. (Upload the `/var/www/stream/live-master-manifest.m3u8` file to the `http://YOUR-WEBSITE.COM`)

Please see **[FFmpeg Protocols Documentation](https://ffmpeg.org/ffmpeg-protocols.html)** for more information.

### Conversion
You can convert your stream to a file or to another stream protocols. You should pass a manifest of a stream to the method:

#### 1. HLS To DASH
```python
import ffmpeg_streaming
from ffmpeg_streaming import Representation

r_360p = Representation(width=640, height=360, kilo_bitrate=276)

(
    ffmpeg_streaming
        .dash('https://www.aminyazdanpanah.com/PATH/TO/HLS-MANIFEST.M3U8')
        .format('libx265')
        .add_rep(r_360p)
        .package('/var/www/media/dash-stream.mpd', progress=progress)
)
```

#### 2. DASH To HLS
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .hls('https://www.aminyazdanpanah.com/PATH/TO/DASH-MANIFEST.MPD')
        .format('libx264')
        .auto_rep(heights=[360, 240])
        .package('/var/www/media/hls-stream.m3u8', progress=progress)
)
```

#### 3. Stream(DASH or HLS) To File
```python
import ffmpeg_streaming

(
    ffmpeg_streaming
        .stream2file('https://www.aminyazdanpanah.com/PATH/TO/MANIFEST.MPD or M3U8')
        .format('libx264')
        .save('/var/www/media/new-video.mp4', progress=progress)
)
```

## Several Open Source Players
You can use these libraries to play your streams.
- **WEB**
    - DASH and HLS: 
        - **[Video.js 7](https://github.com/videojs/video.js) - [videojs-http-streaming (VHS)](https://github.com/videojs/http-streaming)**
        - **[Plyr](https://github.com/sampotts/plyr)**
        - **[DPlayer](https://github.com/MoePlayer/DPlayer)**
        - **[MediaElement.js](https://github.com/mediaelement/mediaelement)**
        - **[Clappr](https://github.com/clappr/clappr)**
        - **[Shaka Player](https://github.com/google/shaka-player)**
        - **[Flowplayer](https://github.com/flowplayer/flowplayer)**
    - DASH:
        - **[dash.js](https://github.com/Dash-Industry-Forum/dash.js)**
    - HLS: 
        - **[hls.js](https://github.com/video-dev/hls.js)**
- **Android**
    - DASH and HLS: 
        - **[ExoPlayer](https://github.com/google/ExoPlayer)**
- **IOS**
    - DASH: 
        - **[MPEGDASH-iOS-Player](https://github.com/MPEGDASHPlayer/MPEGDASH-iOS-Player)**
    - HLS: 
        - **[Player](https://github.com/piemonte/Player)**
- **Windows, Linux, and macOS**
    - DASH and HLS:
        - **[FFmpeg(ffplay)](https://github.com/FFmpeg/FFmpeg)**
        - **[VLC media player](https://github.com/videolan/vlc)**

As you may know, **[IOS](https://www.apple.com/ios)** does not have native support for DASH. Although there are some libraries such as **[Viblast](https://github.com/Viblast/ios-player-sdk)** and **[MPEGDASH-iOS-Player](https://github.com/MPEGDASHPlayer/MPEGDASH-iOS-Player)** to support this technique, I have never tested them. So if you know any IOS player that supports DASH Stream and also works fine, please add it to the above list. 

**NOTE:** You should pass a manifest of stream(e.g. `https://www.aminyazdanpanah.com/PATH_TO_STREAM_DIRECTORY/dash-stream.mpd` or `/PATH_TO_STREAM_DIRECTORY/hls-stream.m3u8` ) to these players.

## Contributing and Reporting Bugs
I'd love your help in improving, correcting, adding to the specification.
Please **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)** or **[submit a pull request](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls)**.
- Please see **[Contributing File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md)** for more information.
- If you have any questions or you want to report a bug, please just **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)**
- If you discover a security vulnerability within this package, please see **[SECURITY File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/SECURITY.md)** for more information.

**NOTE:** If you have any questions about this package or FFmpeg, please **DO NOT** send an email to me (or submit the contact form on my website). Emails regarding these issues **will be ignored**.

## Credits
- **[Amin Yazdanpanah](https://www.aminyazdanpanah.com/?u=github.com/aminyazdanpanah/python-ffmpeg-video-streaming)**
- **[All Contributors](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/graphs/contributors)**

## License
The MIT License (MIT). Please see **[License File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)** for more information.
