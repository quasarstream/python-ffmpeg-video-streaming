import json
import os
import unittest


from ffmpeg_streaming import *
from ffmpeg_streaming.from_clouds import from_url
from ffmpeg_streaming.media import (HLS, DASH)
from ffmpeg_streaming.params import get_hls_parm, get_dash_parm
from ffmpeg_streaming.streams import Streams
import ffmpeg_streaming
from ffmpeg_streaming.progress import progress, get_duration_sec


class TestStreaming(unittest.TestCase):

    def setUp(self):
        self.src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
        self.src_video = os.path.join(self.src_dir, 'test.mp4')
        with open(os.path.join(self.src_dir, 'fixture_ffprobe')) as ffprobe:
            self.ffprobe = json.loads(ffprobe.read())

    def test_ffprobe(self):
        ffprobe = FFProbe(self.src_video)

        all_media = ffprobe.all()

        streams = ffprobe.streams()
        self.assertIsInstance(streams, Streams)
        self.assertEqual(streams.all(), all_media['streams'])
        self.assertEqual(streams.first_stream(), all_media['streams'][0])
        self.assertEqual(streams.video()['codec_type'], 'video')
        self.assertEqual(streams.audio()['codec_type'], 'audio')

    def test_hls(self):
        hls_obj = ffmpeg_streaming.hls(self.src_video)
        self.assertIsInstance(hls_obj, HLS)
        self.assertEqual(hls_obj.filename, self.src_video)
        self.assertEqual(hls_obj.hls_time, 10)
        self.assertEqual(hls_obj.hls_allow_cache, 0)

        hls_obj.add_rep(Representation(width=256, height=144, kilo_bitrate=100))
        rep_1 = hls_obj.reps[0]
        self.assertIsInstance(rep_1, Representation)
        self.assertEqual(rep_1.size, '256x144')
        self.assertEqual(rep_1.bit_rate, '100k')

        hls_obj.auto_rep()
        self.assertEqual(len(hls_obj.reps), 3)
        for rep_ in hls_obj.reps:
            self.assertIsInstance(rep_, Representation)
        rep_1 = hls_obj.reps[0]
        self.assertEqual(rep_1.size, '480x270')
        self.assertEqual(rep_1.bit_rate, '176k')
        rep_2 = hls_obj.reps[1]
        self.assertEqual(rep_2.size, '426x240')
        self.assertEqual(rep_2.bit_rate, '117k')
        rep_3 = hls_obj.reps[2]
        self.assertEqual(rep_3.size, '256x144')
        self.assertEqual(rep_3.bit_rate, '88k')

        hls_obj.format('libx264')
        self.assertEqual(hls_obj.video_format, 'libx264')

        hls_obj.output = hls_obj.filename

        params = get_hls_parm(hls_obj)
        self.assertEqual(len(params), 81)

        hls_obj.package(os.path.join(self.src_dir, 'hls', 'test.m3u8'), capture_stderr=False)
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'hls', 'test.m3u8')) as test_m3u8:
            actual_m3u8 = test_m3u8.read()
        self.assertEqual(actual_m3u8, expected_m3u8)
        with open(os.path.join(self.src_dir, 'hls', 'test_270p.m3u8')) as test_m3u8:
            actual_270_m3u8 = test_m3u8.readlines()
        self.assertEqual(actual_270_m3u8[0].replace('\n', ''), '#EXTM3U')
        self.assertEqual(actual_270_m3u8[1].replace('\n', ''), '#EXT-X-VERSION:3')
        self.assertEqual(actual_270_m3u8[2].replace('\n', ''), '#EXT-X-ALLOW-CACHE:NO')

    def test_encrypted_hls(self):
        encrypted_hls = ffmpeg_streaming.hls(self.src_video).encryption(
            'https://www.aminyazdanpanah.com/enc.key',
            os.path.join(self.src_dir, 'enc.key')
        )

        self.assertIsNotNone(encrypted_hls.hls_key_info_file)

        with open(encrypted_hls.hls_key_info_file) as key_info:
            key_info = key_info.readlines()
        self.assertEqual(key_info[0].replace('\n', ''), 'https://www.aminyazdanpanah.com/enc.key')
        self.assertEqual(key_info[1].replace('\n', ''), os.path.join(self.src_dir, 'enc.key'))

        encrypted_hls.auto_rep()
        encrypted_hls.format('libx264')

        encrypted_hls.package(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8'), capture_stderr=False)
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8')) as test_m3u8:
            actual_encrypted_m3u8 = test_m3u8.read()
        self.assertEqual(actual_encrypted_m3u8, expected_m3u8)

    def test_dash(self):
        dash_obj = ffmpeg_streaming.dash(self.src_video)
        self.assertIsInstance(dash_obj, DASH)
        self.assertEqual(dash_obj.filename, self.src_video)

        dash_obj.auto_rep()
        dash_obj.format('libx265')
        dash_obj.output = dash_obj.filename

        params = get_dash_parm(dash_obj)
        self.assertEqual(len(params), 43)

        dash_obj.package(os.path.join(self.src_dir, 'dash', 'test.mpd'), capture_stderr=False)
        with open(os.path.join(self.src_dir, 'dash', 'test.mpd')) as test_mpd:
            actual_mpd = test_mpd.readlines()
        self.assertEqual(actual_mpd[0].replace('\n', ''), '<?xml version="1.0" encoding="utf-8"?>')
        self.assertEqual(actual_mpd[1].replace('\n', ''), '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')

    def test_progress(self):
        line = 'frame=   00 fps= 0 q=-0.0 q=-0.0 q=-0.0 size=N/A time=00:01:00. bitrate=N/A speed=0.0x'
        total_sec = 60
        _progress = progress(line, total_sec)

        self.assertEqual(_progress, 100)

        d_line = 'Duration: 01:00:00.00, start: 0.000000, bitrate: 0 kb/s'
        _get_duration_sec = get_duration_sec(d_line)

        self.assertEqual(_get_duration_sec, 3600)

    def test_from_clouds(self):
        url = 'https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/_example.mp4' \
              '?raw=true'
        self.assertTrue(os.path.isfile(from_url(url)))


if __name__ == '__main__':
    unittest.main()
