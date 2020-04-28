# 📼 Python FFmpeg Video Streaming
[![Build Status](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming.svg?branch=master)](https://travis-ci.org/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Build status](https://ci.appveyor.com/api/projects/status/qy712tou5pvq629y?svg=true)](https://ci.appveyor.com/project/aminyazdanpanah/python-ffmpeg-video-streaming)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aminyazdanpanah/python-ffmpeg-video-streaming/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aminyazdanpanah/python-ffmpeg-video-streaming/?branch=master)
[![Downloads](https://pepy.tech/badge/python-ffmpeg-video-streaming)](https://pepy.tech/project/python-ffmpeg-video-streaming)
[![PyPI version](https://badge.fury.io/py/python-ffmpeg-video-streaming.svg)](https://badge.fury.io/py/python-ffmpeg-video-streaming)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)

## Overview
This package uses the **[FFmpeg](https://ffmpeg.org)** to package media content for online streaming such as DASH and HLS. You can also use **[DRM](https://en.wikipedia.org/wiki/Digital_rights_management)** for HLS packaging. There are several options to open a file from a cloud and save files to clouds as well.
- **[Full Documentation](https://video.aminyazdanpanah.com/python/)** is available describing all features and components.
- In this version(>=v0.1.0) all codes are rewritten from scratch. If you find any bugs in the library, please **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)**. **[Pull requests](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls)** are also welcome.
 
**Contents**
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Opening a Resource](#opening-a-resource)
  - [DASH](#dash)
  - [HLS](#hls)
    - [Encryption(DRM)](#encryptiondrm)
  - [Transcoding](#transcoding)
  - [Saving Files](#saving-files)
  - [Metadata](#metadata)
  - [Conversion](#conversion)
- [Several Open Source Players](#several-open-source-players)
- [Contributing and Reporting Bugs](#contributing-and-reporting-bugs)
- [Credits](#credits)
- [License](#license)

## Requirements
1. This version of the package is only compatible with **[Python 3.6](https://www.python.org/downloads/)** or higher.

2. To use this package, you need to **[install the FFmpeg](https://ffmpeg.org/download.html)**. You will need both FFmpeg and FFProbe binaries to use it.

## Installation
Install the package via **[pip](https://pypi.org/project/pip/)**:
``` bash
pip install python-ffmpeg-video-streaming
```
Alternatively, add the dependency directly to your `requirements.txt` file:
``` txt
python-ffmpeg-video-streaming>=0.1
```

## Quickstart
First of all, you need to import the package in your code:
```python
import ffmpeg_streaming
```

### Opening a Resource
There are several ways to open a resource.

#### 1. From a FFmpeg supported resource
You can pass a local path of video(or a supported resource) to the `input` method:
```python
video = ffmpeg_streaming.input('/var/media/video.mp4')
```

See **[FFmpeg Protocols Documentation](https://ffmpeg.org/ffmpeg-protocols.html)** for more information about supported resources such as http, ftp, and etc.

**For example:** 
```python
video = ffmpeg_streaming.input('https://www.aminyazdanpanah.com/?"PATH TO A VIDEO FILE" or "PATH TO A LIVE HTTP STREAM"')
```

#### 2. From Clouds
You can open a file from a cloud by passing an instance of a cloud configuration to the `input` method. 

```python
from ffmpeg_streaming import S3
s3 = S3(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET', region_name='YOUR_REGION')

video = ffmpeg_streaming.input(s3, bucket_name="bucket-name", key="video.mp4")
```
Visit **[this page](https://video.aminyazdanpanah.com/python/start/clouds?r=open)** to see some examples of opening a file from **[Amazon S3](https://aws.amazon.com/s3)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud.

#### 3. Capture Webcam or Screen (Live Streaming)
You can pass a name of the supported, connected capture device(i.e. a name of webcam, camera, screen and etc) to the `input` method to stream a live media over network from your connected device. 

 ```python
capture = ffmpeg_streaming.input('CAMERA NAME OR SCREEN NAME', capture=True)
 ```
To list the supported, connected capture devices, see **[FFmpeg Capture Webcam](https://trac.ffmpeg.org/wiki/Capture/Webcam)** and **[FFmpeg Capture Desktop](https://trac.ffmpeg.org/wiki/Capture/Desktop)**.
 
 
### DASH
**[Dynamic Adaptive Streaming over HTTP (DASH)](http://dashif.org/)**, also known as MPEG-DASH, is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers. [Learn more](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)
 
Create DASH files:
```python
from ffmpeg_streaming import Formats

dash = video.dash(Formats.h264())
dash.auto_generate_representations()
dash.output('/var/media/dash.mpd')
```
Generate representations manually:
```python
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

_144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
_240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
_360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
_480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
_1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
_2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
_4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

dash = video.dash(Formats.h264())
dash.representations(_144p, _240p, _360p, _480p, _720p, _1080p, _2k, _4k)
dash.output('/var/media/dash.mpd')
```
See **[DASH section](https://video.aminyazdanpanah.com/python/start?r=dash#dash)** in the documentation, for more examples.

### HLS
**[HTTP Live Streaming (also known as HLS)](https://developer.apple.com/streaming/)** is an HTTP-based adaptive bitrate streaming communications protocol implemented by Apple Inc. as part of its QuickTime, Safari, OS X, and iOS software. Client implementations are also available in Microsoft Edge, Firefox and some versions of Google Chrome. Support is widespread in streaming media servers. [Learn more](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)
 
Create HLS files:
```python
from ffmpeg_streaming import Formats

hls = video.hls(Formats.h264())
hls.auto_generate_representations()
hls.output('/var/media/hls.m3u8')
```
Generate representations manually:
```python
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

_360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
_480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))

hls = video.hls(Formats.h264())
hls.representations(_360p, _480p, _720p)
hls.output('/var/media/hls.m3u8')
```
See **[HLS section](https://video.aminyazdanpanah.com/python/start?r=hls#hls)** in the documentation, for more examples such as Fragmented MP4, live from camera/screen and so on.

#### Encryption(DRM)
The encryption process requires some kind of secret (key) together with an encryption algorithm. HLS uses AES in cipher block chaining (CBC) mode. This means each block is encrypted using the ciphertext of the preceding block. [Learn more](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

You must specify a path to save a random key to your local machine and also a URL(or a path) to access the key on your website(the key you will save must be accessible from your website). You must pass both these parameters to the `encryption` method:

##### Single Key
The following code generates a key for all segment files.

```python
from ffmpeg_streaming import Formats

#A path you want to save a random key to your local machine
save_to = '/home/public_html/"PATH TO THE KEY DIRECTORY"/key'

#A URL (or a path) to access the key on your website
url = 'https://www.aminyazdanpanah.com/?"PATH TO THE KEY DIRECTORY"/key'
# or url = '/"PATH TO THE KEY DIRECTORY"/key';

hls = video.hls(Formats.h264())
hls.encryption(save_to, url)
hls.auto_generate_representations()
hls.output('/var/media/hls.m3u8')
```

##### Key Rotation
An integer as a "key rotation period" can also be passed to the `encryption` method (i.e. `encryption(save_to, url, 10)`) to use a different key for each set of segments, rotating to a new key after this many segments. For example, if 10 segment files have been generated then it will generate a new key. If you set this value to **`1`**, each segment file will be encrypted with a new encryption key. This can improve security and allows for more flexibility. 

See **[the example](https://video.aminyazdanpanah.com/python/start?r=enc-hls#hls-encryption)** for more information.

**IMPORTANT:** It is very important to protect your key(s) on your website. For example, you can use a token(using a Get or Post HTTP method) to check if the user is eligible to access to the key or not. You can also use a session(or cookie) on your website to restrict access to the key(s)(**It is highly recommended**).    

##### DRM
However FFmpeg supports AES encryption for HLS packaging, which you can encrypt your content, it is not a full **[DRM](https://en.wikipedia.org/wiki/Digital_rights_management)** solution. If you want to use a full DRM solution, I recommend trying **[FairPlay Streaming](https://developer.apple.com/streaming/fps/)** solution which then securely exchange keys, and protect playback on devices.

**Besides [Apple's FairPlay](https://developer.apple.com/streaming/fps/)** DRM system, you can also use other DRM systems such as **[Microsoft's PlayReady](https://www.microsoft.com/playready/overview/)** and **[Google's Widevine](https://www.widevine.com/)**.

### Transcoding
You can get realtime information about the transcoding using the following code. 
```python
from ffmpeg_streaming import Formats
import sys

def monitor(ffmpeg, duration, time_):
    per = round(time_ / duration * 100)
    sys.stdout.write("\rTranscoding...(%s%%) [%s%s]" % (per, '#' * per, '-' * (100 - per)))
    sys.stdout.flush()

hls = video.hls(Formats.h264())
hls.auto_generate_representations()
hls.output('/var/media/hls.m3u8', monitor=monitor)
```

##### Output From a Terminal:
![transcoding](https://github.com/aminyazdanpanah/aminyazdanpanah.github.io/blob/master/video-streaming/transcoding.gif?raw=true "transcoding" )

### Saving Files
There are several ways to save files.

#### 1. To a Local Path
You can pass a local path to the `output` method. If there is no directory, then the package will create it.
```python
from ffmpeg_streaming import Formats

dash = video.dash(Formats.h264())
dash.auto_generate_representations()

dash.output('/var/media/dash.mpd')
```
It can also be None. The default path to save files is the input directory.
```python
from ffmpeg_streaming import Formats

hls = video.hls(Formats.h264())
hls.auto_generate_representations()

hls.output()
```
**NOTE:** If you open a file from a cloud and do not pass a path to save the file to your local machine, you will have to pass a local path to the `output` method.

#### 2. To Clouds
You can save your files to a cloud by passing an instance of a `CloudManager` to the `output` method. 

```python
from ffmpeg_streaming import  S3, CloudManager

s3 = S3(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET', region_name='YOUR_REGION')
save_to_s3 = CloudManager().add(s3, bucket_name="bucket-name")

hls.output(clouds=save_to_s3)
``` 
A path can also be passed to save a copy of files to your local machine.
```python
hls.output('/var/media/hls.m3u8', clouds=save_to_s3)
```

Visit **[this page](https://video.aminyazdanpanah.com/python/start/clouds?r=save)** to see some examples of saving files to **[Amazon S3](https://aws.amazon.com/s3)**, **[Google Cloud Storage](https://console.cloud.google.com/storage)**, **[Microsoft Azure Storage](https://azure.microsoft.com/en-us/features/storage-explorer/)**, and a custom cloud. 

**NOTE:** This option is only valid for **[VOD](https://en.wikipedia.org/wiki/Video_on_demand)** (it does not support live streaming).

**Schema:** The relation is `one-to-many`

<p align="center"><img src="https://github.com/aminyazdanpanah/aminyazdanpanah.github.io/blob/master/video-streaming/video-streaming.gif?raw=true" width="100%"></p>

#### 3. To a Server Instantly
You can pass a url(or a supported resource like `ftp`) to the `output` method to upload all the segments files to the HTTP server(or other protocols) using the HTTP PUT method, and update the manifest files every refresh times.

```python
# DASH
dash.output('http://YOUR-WEBSITE.COM/live-stream/out.mpd')

# HLS
hls.output('http://YOUR-WEBSITE.COM/live-stream/out.m3u8')
```

**NOTE:** In the HLS method, you must upload the master playlist to the server manually.

See **[FFmpeg Protocols Documentation](https://ffmpeg.org/ffmpeg-protocols.html)** for more information about supported resources.

### Metadata
You can get information from the video file using the following code.
```python
from ffmpeg_streaming import FFProbe

ffprobe = FFProbe('/var/media/video.mp4')
```

See **[the example](https://video.aminyazdanpanah.com/python/start?r=metadata#metadata)** for more information.

### Conversion
You can convert your stream to a file or to another stream protocols. You should pass a manifest of the stream to the `input` method:

#### 1. HLS To DASH
```python
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

video = ffmpeg_streaming.input('https://www.aminyazdanpanah.com/?PATH/TO/HLS-MANIFEST.M3U8')

_480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))

dash = video.dash(Formats.h264())
dash.representations(_480p)
dash.output('/var/media/dash.mpd')
```

#### 2. DASH To HLS
```python
video = ffmpeg_streaming.input('https://www.aminyazdanpanah.com/?PATH/TO/DASH-MANIFEST.MPD')

hls = video.hls(Formats.h264())
hls.auto_generate_representations()
hls.output('/var/media/hls.m3u8')
```

#### 3. Stream(DASH or HLS) To File
```python
video = ffmpeg_streaming.input('https://www.aminyazdanpanah.com/?PATH/TO/MANIFEST.MPD or M3U8')

stream = video.stream2file(Formats.h264())
stream.output('/var/media/new-video.mp4')
```

## Several Open Source Players
You can use these libraries to play your streams.
- **WEB**
    - DASH and HLS: 
        - **[Video.js 7](https://github.com/videojs/video.js) (Recommended) - [videojs-http-streaming (VHS)](https://github.com/videojs/http-streaming)**
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

**NOTE-1:** You must pass a **link of the master playlist(manifest)**(i.e. `https://www.aminyazdanpanah.com/?"PATH TO STREAM DIRECTORY"/dash-stream.mpd` or `/PATH_TO_STREAM_DIRECTORY/hls-stream.m3u8` ) to these players.

**NOTE-2:** If you save your stream content to a cloud(i.e. **[Amazon S3](https://aws.amazon.com/s3)**), the link of your playlist and other content **MUST BE PUBLIC**. 

**NOTE-3:** As you may know, **[IOS](https://www.apple.com/ios)** does not have native support for DASH. Although there are some libraries such as **[Viblast](https://github.com/Viblast/ios-player-sdk)** and **[MPEGDASH-iOS-Player](https://github.com/MPEGDASHPlayer/MPEGDASH-iOS-Player)** to support this technique, I have never tested them. So maybe som of them will not work correctly.


## Contributing and Reporting Bugs
I'd love your help in improving, correcting, adding to the specification. Please **[file an issue](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/issues)** or **[submit a pull request](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/pulls)**.
- See **[Contributing File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md)** for more information.
- If you discover a security vulnerability within this package, please see **[SECURITY File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/SECURITY.md)** for more information.

## Credits
- **[Amin Yazdanpanah](https://www.aminyazdanpanah.com/?u=github.com/aminyazdanpanah/python-ffmpeg-video-streaming)**
- **[All Contributors](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/graphs/contributors)**

## License
The MIT License (MIT). See **[License File](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/LICENSE)** for more information.
