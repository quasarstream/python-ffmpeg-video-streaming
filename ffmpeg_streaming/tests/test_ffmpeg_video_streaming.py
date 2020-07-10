import json
import os
import unittest

import ffmpeg_streaming
from ffmpeg_streaming import Formats
from ffmpeg_streaming import FFProbe, Representation, Size, Bitrate
from ffmpeg_streaming._media import HLS, DASH
from ffmpeg_streaming.ffprobe import Streams


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
        video = ffmpeg_streaming.input(self.src_video)
        hls_obj = video.hls(Formats.h264())
        self.assertIsInstance(hls_obj, HLS)
        self.assertEqual(hls_obj.media.input, self.src_video)

        hls_obj.representations(Representation(Size(256, 144), Bitrate(102400)))
        rep_1 = hls_obj.reps[0]
        self.assertIsInstance(rep_1, Representation)
        self.assertEqual(str(rep_1.size), '256x144')
        self.assertEqual(rep_1.bitrate.video, '100k')

        hls_obj.auto_generate_representations()
        reps = list(hls_obj.reps)
        self.assertEqual(len(reps), 3)

        for rep_ in reps:
            self.assertIsInstance(rep_, Representation)
        self.assertEqual(str(reps[0].size), '480x270')
        self.assertEqual(reps[0].bitrate.video, '176k')
        self.assertEqual(str(reps[1].size), '426x240')
        self.assertEqual(reps[1].bitrate.video, '88k')
        self.assertEqual(str(reps[2].size), '256x144')
        self.assertEqual(reps[2].bitrate.video, '71k')

        hls_obj.output(os.path.join(self.src_dir, 'hls', 'test.m3u8'))
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'hls', 'test.m3u8')) as test_m3u8:
            actual_m3u8 = test_m3u8.read()
        self.assertEqual(actual_m3u8, expected_m3u8)
        with open(os.path.join(self.src_dir, 'hls', 'test_270p.m3u8')) as test_m3u8:
            actual_270_m3u8 = test_m3u8.readlines()
        self.assertEqual(actual_270_m3u8[0].replace('\n', ''), '#EXTM3U')
        self.assertEqual(actual_270_m3u8[1].replace('\n', ''), '#EXT-X-VERSION:3')
        self.assertEqual(actual_270_m3u8[2].replace('\n', ''), '#EXT-X-ALLOW-CACHE:YES')

    def test_encrypted_hls(self):
        video = ffmpeg_streaming.input(self.src_video)
        hls_obj = video.hls(Formats.h264())
        hls_obj.encryption(os.path.join(self.src_dir, 'enc.key'), 'https://www.aminyazdanpanah.com/enc.key')

        self.assertIsNotNone(hls_obj.options.get('hls_key_info_file', None))

        with open(hls_obj.options.get('hls_key_info_file', None)) as key_info:
            key_info = key_info.readlines()
        self.assertEqual(key_info[0].replace('\n', ''), 'https://www.aminyazdanpanah.com/enc.key')
        self.assertEqual(key_info[1].replace('\n', ''), os.path.join(self.src_dir, 'enc.key'))

        hls_obj.auto_generate_representations()

        hls_obj.output(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8'), stderr=False)
        with open(os.path.join(self.src_dir, 'fixture_test.m3u8')) as test_m3u8:
            expected_m3u8 = test_m3u8.read()
        with open(os.path.join(self.src_dir, 'encrypted_hls', 'test.m3u8')) as test_m3u8:
            actual_encrypted_m3u8 = test_m3u8.read()
        self.assertEqual(actual_encrypted_m3u8, expected_m3u8)

    def test_dash(self):
        video = ffmpeg_streaming.input(self.src_video)
        dash_obj = video.dash(Formats.hevc())
        self.assertIsInstance(dash_obj, DASH)
        self.assertEqual(dash_obj.media.input, self.src_video)

        dash_obj.auto_generate_representations()

        dash_obj.output(os.path.join(self.src_dir, 'dash', 'test.mpd'), stderr=False)
        with open(os.path.join(self.src_dir, 'dash', 'test.mpd')) as test_mpd:
            actual_mpd = test_mpd.readlines()
        self.assertEqual(actual_mpd[0].replace('\n', ''), '<?xml version="1.0" encoding="utf-8"?>')
        self.assertEqual(actual_mpd[1].replace('\n', ''), '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')


if __name__ == '__main__':
    unittest.main()
