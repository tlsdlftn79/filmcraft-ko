#!/usr/bin/env python3
"""RC14 post-export hardware encoder regression checks (no GPU required)."""
import importlib.util
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('gpu_mp4_transcode.py')
spec = importlib.util.spec_from_file_location('gpu_mp4_transcode', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestRc14GpuTranscode(unittest.TestCase):
    def test_explicit_backend_does_not_silently_change_gpu(self):
        have = {'h264_nvenc', 'h264_qsv', 'libx264'}
        self.assertEqual(mod.candidate_backends('amd', have, False), [])
        self.assertEqual(mod.candidate_backends('intel', have, False), ['intel'])
        self.assertEqual(mod.candidate_backends('amd', have, True), ['cpu'])

    def test_auto_order_and_fallback_are_explicit(self):
        have = {'h264_amf', 'h264_qsv', 'libx264'}
        self.assertEqual(mod.candidate_backends('auto', have, False), ['amd', 'intel'])
        self.assertEqual(mod.candidate_backends('auto', have, True), ['amd', 'intel', 'cpu'])

    def test_output_preserves_audio_and_mp4(self):
        c = mod.encode_command('ffmpeg', Path('입력.mp4'), Path('출력.mp4'), 'amd', 12000, False)
        self.assertEqual(c[c.index('-c:v') + 1], 'h264_amf')
        self.assertEqual(c[c.index('-c:a') + 1], 'copy')
        self.assertIn('0:a?', c)
        self.assertIn('0:s?', c)
        self.assertEqual(c[c.index('-c:s') + 1], 'mov_text')
        self.assertEqual(c[c.index('-f') + 1], 'mp4')

    def test_shorts_dimensions_keep_fps(self):
        c = mod.encode_command('ffmpeg', Path('in.mp4'), Path('out.mp4'), 'intel', 12000, True)
        vf = c[c.index('-vf') + 1]
        self.assertIn('scale=1080:1920:force_original_aspect_ratio=increase', vf)
        self.assertIn('crop=1080:1920', vf)
        self.assertIn('format=nv12', vf)
        self.assertNotIn('-r', c)

    def test_invalid_bitrate_fails(self):
        with self.assertRaises(ValueError):
            mod.encode_command('ffmpeg', Path('a.mp4'), Path('b.mp4'), 'amd', 0, False)

    def test_cannot_overwrite_original_or_existing_file(self):
        with tempfile.TemporaryDirectory() as p:
            src = Path(p) / '기존 자막.mp4'
            src.write_bytes(b'dummy')
            with self.assertRaises(ValueError):
                mod.transcode(src, src, 'cpu', 1000, False, False, 'ffmpeg', 'ffprobe')
            dst = Path(p) / 'out.mp4'
            dst.write_bytes(b'existing')
            with self.assertRaises(FileExistsError):
                mod.transcode(src, dst, 'cpu', 1000, False, False, 'ffmpeg', 'ffprobe')

    def test_no_gpu_or_cpu_encoders_fails_clearly(self):
        with tempfile.TemporaryDirectory() as p:
            src = Path(p) / 'src.mp4'
            src.write_bytes(b'dummy')
            with patch.object(mod, 'video_details', return_value={'width': 10, 'height': 10}), patch.object(mod, 'available_encoders', return_value=set()):
                with self.assertRaisesRegex(RuntimeError, 'No requested FFmpeg'):
                    mod.transcode(src, Path(p) / 'out.mp4', 'amd', 12000, False, False, 'ffmpeg', 'ffprobe')

if __name__ == '__main__':
    unittest.main(verbosity=2)
