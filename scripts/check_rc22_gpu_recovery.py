#!/usr/bin/env python3
"""RC22 source-level safety regression checks (NOT a Rust/Windows build)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GPU = (ROOT / 'crates/engine/src/hardware_transcode.rs').read_text(encoding='utf-8')
EXPORT = (ROOT / 'crates/engine/src/export_tools.rs').read_text(encoding='utf-8')

class GpuRecoveryChecks(unittest.TestCase):
    def test_stale_backup_is_not_unconditionally_deleted(self):
        section = GPU.split('fn replace_file(', 1)[1].split('/// Do hardware encode', 1)[0]
        self.assertIn('if backup.exists()', section)
        self.assertIn('prior export recovery backup exists', section)
        self.assertNotIn('let _ = std::fs::remove_file(&backup)', section)

    def test_failed_rollback_keeps_recovery_path_in_diagnostic(self):
        self.assertIn('previous output is preserved at {}', GPU)
        self.assertIn('backup.display()', GPU)
        self.assertIn('restoration failed:', GPU)

    def test_staged_cpu_mp4_is_retained_on_errors(self):
        self.assertIn('recoverable CPU MP4 retained at {}', EXPORT)
        self.assertIn('(!gpu_finish_started || prog.cancel.load(Ordering::Relaxed))', EXPORT)
        self.assertIn('if prog.cancel.load(Ordering::Relaxed) || e == "cancelled"', EXPORT)

    def test_rust_filesystem_regression_tests(self):
        for name in ('stale_recovery_backup_is_never_overwritten_or_deleted',
                     'newly_created_output_needs_no_previous_backup',
                     'replacing_file_with_itself_is_rejected'):
            self.assertIn('fn ' + name + '(', GPU)

    def test_gpu_paths_still_integrated(self):
        for name in ('h264_amf', 'h264_qsv', 'fn checked_command_with_output(',
                     'fn verify(', 'fn replace_file('):
            self.assertIn(name, GPU)
        self.assertIn('hardware_transcode::finish(', EXPORT)

    def test_version_and_distributables(self):
        installer = (ROOT / 'packaging/windows/filmcraft-korean.iss').read_text(encoding='utf-8')
        verify = (ROOT / 'scripts/verify_release.py').read_text(encoding='utf-8')
        self.assertIn('#define PatchChannel "Stable"', installer)
        self.assertIn("VERSION = '0.6.0_Stable'", verify)

if __name__ == '__main__':
    unittest.main(verbosity=2)
