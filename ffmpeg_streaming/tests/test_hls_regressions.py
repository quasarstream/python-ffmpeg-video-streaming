import os
import shutil
import tempfile
import unittest

import ffmpeg_streaming
from ffmpeg_streaming import Bitrate, Formats, Representation, Size
from ffmpeg_streaming._command_builder import _hls
from ffmpeg_streaming._hls_helper import HLSKeyInfoFile, HLSMasterPlaylist


class TestHLSRegressions(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="hls_reg_")
        self.src_video = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "files", "test.mp4"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_master_playlist_matches_command_builder_for_dotted_filenames(self):
        video = ffmpeg_streaming.input(self.src_video)
        hls_obj = video.hls(Formats.h264())
        hls_obj.representations(
            Representation(Size(1280, 720), Bitrate(2048 * 1024)),
            Representation(Size(854, 480), Bitrate(1024 * 1024)),
        )
        dotted_output = os.path.join(self.tmp_dir, "episode.01.v2.m3u8")
        hls_obj.output(dotted_output, run_command=False)

        with open(dotted_output, encoding="utf-8") as fp:
            manifest = fp.read()

        cmd_args = _hls(hls_obj)
        self.assertIn(os.path.join(self.tmp_dir, "episode.01.v2_720p.m3u8"), cmd_args)
        self.assertIn("episode.01.v2_720p.m3u8", manifest)
        self.assertIn("episode.01.v2_480p.m3u8", manifest)
        self.assertEqual(
            HLSMasterPlaylist(hls_obj).sub_path(hls_obj.reps[0]),
            ["episode.01.v2_720p_vtt.m3u8"],
        )

    def test_hls_instances_isolate_master_playlist_and_key_info_state(self):
        video = ffmpeg_streaming.input(self.src_video)

        hls_first = video.hls(Formats.h264())
        hls_first.representations(Representation(Size(640, 360), Bitrate(512 * 1024)))
        custom_master = os.path.join(self.tmp_dir, "custom_first.m3u8")
        hls_first.save_master_playlist(custom_master)
        hls_first.encryption(
            os.path.join(self.tmp_dir, "first.key"),
            "https://cdn.example.com/first.key",
        )

        hls_second = video.hls(Formats.h264())
        hls_second.representations(Representation(Size(640, 360), Bitrate(512 * 1024)))
        second_master = os.path.join(self.tmp_dir, "second_auto.m3u8")
        hls_second.output(second_master, run_command=False)

        self.assertTrue(os.path.isfile(custom_master))
        self.assertTrue(os.path.isfile(second_master))

        hls_second.encryption(
            os.path.join(self.tmp_dir, "second.key"),
            "https://cdn.example.com/second.key",
        )
        self.assertNotEqual(
            hls_first.KEY_INFO_FILE_PATH, hls_second.KEY_INFO_FILE_PATH
        )

        hls_first.finish_up()
        self.assertFalse(os.path.exists(hls_first.KEY_INFO_FILE_PATH))
        self.assertTrue(os.path.exists(hls_second.KEY_INFO_FILE_PATH))
        hls_second.finish_up()

    def test_rotate_key_ignores_non_positive_period(self):
        key_path = os.path.join(self.tmp_dir, "enc.key")
        info_path = os.path.join(self.tmp_dir, "enc.keyinfo")
        key_info = HLSKeyInfoFile(
            info_path,
            key_path,
            "https://cdn.example.com/enc.key",
            period=0,
            needle=".ts' for writing",
        )
        key_info.generate()
        initial_url = key_info.url
        key_info.rotate_key("Opening 'seg_0001.ts' for writing")
        self.assertEqual(key_info.url, initial_url)

    def test_bitrate_calc_overall_when_audio_is_copied(self):
        b_video_only = Bitrate(102400)
        self.assertEqual(b_video_only.audio, "copy")
        self.assertEqual(b_video_only.calc_overall, 102400)
        b_both = Bitrate(102400, 65536)
        self.assertEqual(b_both.calc_overall, 167936)


if __name__ == "__main__":
    unittest.main()
