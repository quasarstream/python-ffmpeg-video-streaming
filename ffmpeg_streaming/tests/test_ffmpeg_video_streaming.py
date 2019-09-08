import json
import os
import unittest

from ffmpeg_streaming import *
from ffmpeg_streaming.params import get_hls_parm, get_dash_parm
from ffmpeg_streaming.streams import Streams
import ffmpeg_streaming
from ffmpeg_streaming.progress import progress


class TestStreaming(unittest.TestCase):

    def setUp(self):
        self.src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
        self.src_video = os.path.join(self.src_dir, 'test.mp4')
        with open(os.path.join(self.src_dir, 'fixture_ffprobe')) as ffprobe:
            self.ffprobe = json.loads(ffprobe.read())

    def test_ffprobe(self):
        ffprobe = FFProbe(self.src_video)

        all_media = ffprobe.all()
        del all_media['format']['filename']
        self.assertEqual(all_media, self.ffprobe)

        streams = ffprobe.streams()
        self.assertIsInstance(streams, Streams)
        self.assertEqual(streams.all(), all_media['streams'])
        self.assertEqual(streams.first_stream(), all_media['streams'][0])
        self.assertEqual(streams.video()['codec_type'], 'video')
        self.assertEqual(streams.audio()['codec_type'], 'audio')

    def test_hls(self):
        hls = ffmpeg_streaming.hls(self.src_video)
        self.assertIsInstance(hls, HLS)
        self.assertEqual(hls.filename, self.src_video)
        self.assertEqual(hls.hls_time, 10)
        self.assertEqual(hls.hls_allow_cache, 0)

        hls.add_rep(Representation(width=256, height=144, kilo_bitrate=100))
        rep = hls.reps[0]
        self.assertIsInstance(rep, Representation)
        self.assertEqual(rep.size(), '256x144')
        self.assertEqual(rep.bit_rate(), '100k')

        hls.auto_rep()
        self.assertEqual(len(hls.reps), 3)
        for rep in hls.reps:
            self.assertIsInstance(rep, Representation)
        rep_1 = hls.reps[0]
        self.assertEqual(rep_1.size(), '480x270')
        self.assertEqual(rep_1.bit_rate(), '176k')
        rep_2 = hls.reps[1]
        self.assertEqual(rep_2.size(), '426x240')
        self.assertEqual(rep_2.bit_rate(), '117k')
        rep_3 = hls.reps[2]
        self.assertEqual(rep_3.size(), '256x144')
        self.assertEqual(rep_3.bit_rate(), '88k')

        hls.format('libx264')
        self.assertEqual(hls.format, 'libx264')

        hls.path = hls.filename

        params = get_hls_parm(hls)
        self.assertEqual(len(params), 75)

        hls.package(os.path.join(self.src_dir, 'hls', 'test.m3u8'))
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'hls', 'test.m3u8')) as test_m3u8:
            actual_m3u8 = test_m3u8.read()
        self.assertEqual(actual_m3u8, expected_m3u8)
        with open(os.path.join(self.src_dir, 'fixture_test_270p.m3u8')) as test_m3u8:
            expected_270_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'hls', 'test_270p.m3u8')) as test_m3u8:
            actual_270_m3u8 = test_m3u8.read()
        self.assertEqual(actual_270_m3u8, expected_270_m3u8)

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

        encrypted_hls.package(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8'))
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8')) as test_m3u8:
            actual_encrypted_m3u8 = test_m3u8.read()
        self.assertEqual(actual_encrypted_m3u8, expected_m3u8)

    def test_dash(self):
        dash = ffmpeg_streaming.dash(self.src_video)
        self.assertIsInstance(dash, DASH)
        self.assertEqual(dash.filename, self.src_video)

        dash.auto_rep()
        dash.format('libx265')
        dash.path = dash.filename

        params = get_dash_parm(dash)
        self.assertEqual(len(params), 37)

        dash.package(os.path.join(self.src_dir, 'dash', 'test.mpd'))
        with open(os.path.join(self.src_dir, 'dash', 'test.mpd')) as test_mpd:
            actual_mpd = test_mpd.readlines()
        self.assertEqual(actual_mpd[0].replace('\n', ''), '<?xml version="1.0" encoding="utf-8"?>')
        self.assertEqual(actual_mpd[1].replace('\n', ''), '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')

    def test_progress(self):
        line = 'frame=   00 fps= 0 q=-0.0 q=-0.0 q=-0.0 size=N/A time=00:01:00. bitrate=N/A speed=0.0x'
        total_sec = 60
        _progress = progress(line, total_sec)

        self.assertEqual(_progress, 100)


if __name__ == '__main__':
    unittest.main()
