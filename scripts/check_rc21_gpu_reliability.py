#!/usr/bin/env python3
"""RC22 static safety checks, NOT a Windows/Rust/GPU runtime pass."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class GpuExportReliability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gpu = (ROOT/'crates/engine/src/hardware_transcode.rs').read_text(encoding='utf-8')
        cls.engine = (ROOT/'crates/engine/src/export_tools.rs').read_text(encoding='utf-8')
        cls.graphics = (ROOT/'crates/ui-egui/src/panels/graphics.rs').read_text(encoding='utf-8')

    def test_ffprobe_is_cancellable(self):
        self.assertIn('checked_command_with_output(probe_cmd, cancel', self.gpu)
        self.assertNotIn('Command::new("ffprobe")\n        .args', self.gpu)
        self.assertIn('if cancel.load(Ordering::Relaxed)', self.gpu)

    def test_stderr_drain_does_not_deadlock_or_exhaust_memory(self):
        self.assertIn('fn read_error_tail', self.gpu)
        self.assertIn('stderr(Stdio::piped())', self.gpu)
        self.assertIn('const LIMIT: usize = 8192', self.gpu)
        self.assertIn('std::thread::spawn(move || read_error_tail(stderr))', self.gpu)

    def test_cpu_fallback_stays_available(self):
        self.assertIn('if verified { &candidate } else { source }', self.gpu)
        self.assertIn('if source == dest', self.gpu)
        self.assertIn('CPU source MP4 is missing or empty', self.gpu)
        self.assertIn('fn replace_file', self.gpu)

    def test_rust_regression_tests_present(self):
        for test in ('errors_keep_only_bounded_stderr_tail',
                     'replace_file_keeps_existing_output_on_failed_candidate',
                     'successful_replace_retires_old_output'):
            self.assertIn('fn '+test, self.gpu)

    def test_app_integration_and_ime_stays(self):
        self.assertIn('hardware_transcode::finish(', self.engine)
        self.assertIn('h264_amf', self.gpu)
        self.assertIn('h264_qsv', self.gpu)
        self.assertEqual(self.graphics.count('fn has_ime_edit('), 1)
        self.assertIn('fn has_ime_edit(', self.graphics.split('mod korean_ime_tests {',1)[1])

    def test_release_identity(self):
        self.assertIn("VERSION = '0.6.0_Stable'", (ROOT/'scripts/verify_release.py').read_text())
        self.assertIn('#define PatchChannel "Stable"', (ROOT/'packaging/windows/filmcraft-korean.iss').read_text())
        self.assertIn('FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe', (ROOT/'scripts/build-installer.ps1').read_text())

if __name__=='__main__':
    unittest.main(verbosity=2)
