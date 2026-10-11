#!/usr/bin/env python3
"""RC22 source guard: path validation and version alignment (not a Rust build)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Rc18SourceChecks(unittest.TestCase):
    def test_export_rejects_invalid_destinations_without_closing(self):
        source = read("crates/ui-egui/src/panels/export_mode.rs")
        self.assertIn("fn valid_windows_export_path(path: &str) -> bool", source)
        self.assertIn("if go && !valid_windows_export_path(&app.ui.export.quick_path)", source)
        self.assertIn("} else if go {", source)
        self.assertIn("mod rc18_export_path_tests", source)
        self.assertIn("Some(\'C\'), Some(\'O\'), Some(\'M\')", source)
        self.assertIn("Some(\'L\'), Some(\'P\'), Some(\'T\')", source)
        self.assertIn('"한글 쇼츠.mp4"', source)
        self.assertIn('tl!("Select a valid Windows export filename.")', source)

    def test_korean_error_message(self):
        self.assertIn("\tSelect a valid Windows export filename.\t올바른 Windows", read("crates/ui-egui/src/i18n/ko.tsv"))

    def test_release_identity(self):
        version = "0.6.0_Stable"
        self.assertIn(f"VERSION = '{version}'", read("scripts/verify_release.py"))
        self.assertRegex(read("packaging/windows/filmcraft-korean.iss"), r'#define PatchChannel "Stable"')
        self.assertIn("FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe", read("scripts/build-installer.ps1"))
        self.assertIn("FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip", read("scripts/build-win.ps1"))
        self.assertIn("Stable_Korean_Windows_x64", read(".github/workflows/korean-windows-rc.yml"))

    def test_installer_does_not_delete_user_data(self):
        iss = read("packaging/windows/filmcraft-korean.iss")
        self.assertNotIn("\n[UninstallDelete]", iss)
        self.assertIn("PrivilegesRequired=lowest", iss)
        self.assertIn("DefaultDirName={localappdata}", iss)

    def test_ime_text_only_helpers_remain_test_gated(self):
        source = read("crates/ui-egui/src/panels/graphics.rs")
        self.assertRegex(source, r'#\[cfg\(test\)\]\s*mod korean_ime_tests \{[\s\S]*?fn has_ime_edit\(')
        self.assertNotIn("ImeEvent::Disabled", source)
        self.assertIn("ImeFrameEchoBudget::new(&events)", source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
