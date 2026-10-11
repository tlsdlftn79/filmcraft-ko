#!/usr/bin/env python3
"""RC22 structural regression guards. These are NOT Rust/Windows runtime tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding="utf-8")

class Rc19Checks(unittest.TestCase):
    def test_export_validation_covers_parent_components(self):
        s = read("crates/ui-egui/src/panels/export_mode.rs")
        self.assertIn("parts[from..].iter().all(|part| valid_windows_filename_part(part))", s)
        self.assertIn("fn valid_windows_filename_part(part: &str) -> bool", s)
        self.assertIn("(resp.clicked() || qresp.clicked()) && !valid_windows_export_path", s)
        self.assertIn("fn rejects_invalid_parent_folders_and_win32_device_names()", s)
        self.assertIn("fn allows_unicode_windows_absolute_relative_and_unc_paths()", s)
        self.assertIn("COM¹.mp4", s)
        self.assertIn("가을.mp4", s)

    def test_windows_separator_extension_preserves_parent_folder(self):
        s = read("crates/ui-egui/src/panels/export_mode.rs")
        self.assertIn("let file_start = path.rfind(", s)
        self.assertIn("folder.v2", s)
        self.assertIn("quick_path_with_extension", s)

    def test_release_identity_stays_consistent(self):
        self.assertIn("VERSION = '0.6.0_Stable'", read('scripts/verify_release.py'))
        self.assertRegex(read('packaging/windows/filmcraft-korean.iss'), r'#define PatchChannel "Stable"')
        self.assertIn("FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip", read('scripts/build-win.ps1'))
        self.assertIn("FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe", read('scripts/build-installer.ps1'))
        self.assertIn('rc19-windows-acceptance.ps1', read('RC19_TEST_GUIDE_KO.md'))

    def test_preserve_core_user_features_without_claiming_gpu_encoding(self):
        links = read('crates/ui-egui/src/links.rs')
        self.assertIn('https://ctee.kr/place/caw', links)
        self.assertIn('https://discord.gg/artcraft', links)
        self.assertIn('ImeFrameEchoBudget::new(&events)', read('crates/ui-egui/src/panels/graphics.rs'))
        self.assertIn('YouTube Shorts', read('crates/engine/src/export_tests.rs'))
        self.assertIn('PrivilegesRequired=lowest', read('packaging/windows/filmcraft-korean.iss'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
