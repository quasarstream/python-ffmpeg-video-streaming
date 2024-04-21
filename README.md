# 📼 Python FFmpeg Video Streaming

[![Downloads](https://pepy.tech/badge/python-ffmpeg-video-streaming)](https://pepy.tech/project/python-ffmpeg-video-streaming)

<p align="center"><img src="https://github.com/quasarstream/quasarstream.github.io/blob/master/video-streaming/video-streaming-v2.gif?raw=true" width="100%"></p>

This package utilizes **[FFmpeg](https://ffmpeg.org)**  to bundle media content for online streaming, including DASH and
HLS. Additionally, it provides the capability to implement **[DRM](https://en.wikipedia.org/wiki/Digital_rights_management)** for HLS packaging. The program offers a range of
options to open files from cloud storage and save files to cloud storage as well.

## Documentation

**[Full Documentation](https://www.quasarstream.com/op/python/ffmpeg-streaming/)** is available describing all features
and components.

## Basic Usage

```python
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

_360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
_480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))

hls = video.hls(Formats.h264())
hls.representations(_360p, _480p, _720p)
hls.output('/var/media/hls.m3u8')
```

## Get from Basic, Pro, and Enterprise packages for Video Streaming

Our service enables you to save a significant amount of time and resources, allowing you to concentrate on the essential
features of your OTT platform without worrying about time-consuming boilerplate code. Our cost-effective solution starts
at **$78**, giving you the flexibility to focus on your core competencies and accelerate your development process. By
utilizing our service, you can improve your productivity, reduce your development time, and deliver top-quality results.
Don't let the burden of writing boilerplate code slow you down; let us help you streamline your development process and
take your OTT platform to the next level.

### Project information

- **BACKEND:** Python - Django v5
- **FRONTEND:** Javascript ES6 - React v18
- **CONTAINER:** Docker

### Plans

<div style="align-content: center">
<table style="margin: auto">
    <thead>
        <tr>
            <th>Features / Plans</th>
            <th>Basic</th>
            <th>Pro</th>
            <th>Enterprise</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>OAuth 2.0 (Login, Register)</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Access-control list (ACL)</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Video On-Demand</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>HLS</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>DASH</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>HLS Encryption(Single key and key rotation)</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Video Quality Settings (Choose from 144p to 4k and auto mode)</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Real-Time Progress Monitoring (progress bar to show the live upload and transcoding progress)</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Dark and light theme</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Live Streaming (From Browser Webcam, IP Cameras, Live Streaming Software)</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Custom player skin</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Monetization: Subscriptons/pay-per-view/ads</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Advanced Analytics: Views/Watched hours/Visited countries and more</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Robust DRM Systems: Widevine, FairPlay Streaming and PlayReady</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Social Media Integration(Like, Comment, Share videos)</td>
            <td align="center">⛔️</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Cloud CDN (Content Delivery Network to Clouds Like Amazon S3, Google Cloud Storage, Microsoft Azure and more)</td>
            <td align="center">⛔️</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Email Service</td>
            <td align="center">⛔️</td>
            <td align="center">⛔️</td>
            <td align="center">✅</td>
        </tr>
        <tr>
            <td>Support</td>
            <td align="center">3 Months</td>
            <td align="center">6 Months</td>
            <td align="center">Customizable</td>
        </tr>
        <tr>
            <td>Price</td>
            <td align="center"><strong title="One-time fee">$78</strong></td>
            <td align="center" colspan="2"><strong title="Start at $198 (monthly fee)">Custom Pricing Available</strong></td>
        </tr>
        <tr>
            <td>Get</td>
            <td align="center"> <strong><a target="_blank" href="https://quasarstream.com/video-streaming-basic?u=py-ffmpeg"> GET THE BASIC PACKAGES</a></strong> </td>
            <td align="center"  colspan="2"> <strong><a target="_blank" href="https://quasarstream.com/contact?u=py-ffmpeg"> CONTACT US</a></strong> </td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <th align="left" colspan="4">
                We have demos available. Please <a target="_blank" href="https://quasarstream.com/contact?u=py-ffmpeg"> CONTACT US</a> to request one.
            </th>
        </tr>
        <tr>
            <th align="left" colspan="4">
                    If you have any questions or doubts, please don't hesitate to contact Amin Yazdanpanah (admin) using <a target="_blank" href="https://aminyazdanpanah.com/?u=py-ffmpeg">this link</a>.            
            </th>
        </tr>
    </tfoot>
</table>
</div>

### Screenshots
<p align="center"><img src="https://github.com/quasarstream/quasarstream.github.io/blob/master/video-streaming/video-streaming-screen-hots.gif?raw=true" width="100%"></p>

## Contributors

Your contribution is crucial to our success, regardless of its size. We appreciate your support and encourage you to
read our **[CONTRIBUTING](https://github.com/quasarstream/python-ffmpeg-video-streaming/blob/master/CONTRIBUTING.md)**
guide for detailed instructions on how to get involved. Together, we can make a significant impact.

<a href="https://github.com/quasarstream/python-ffmpeg-video-streaming/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=quasarstream/python-ffmpeg-video-streaming" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## License

The MIT License (MIT). See **[License File](https://github.com/quasarstream/python-ffmpeg-video-streaming/blob/master/LICENSE)** for more
information.
