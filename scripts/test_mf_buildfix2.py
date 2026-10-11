#!/usr/bin/env python3
"""BuildFix2 source-level regression tests (not a substitute for Windows cargo check).

Run from any directory: python scripts/test_mf_buildfix2.py
Uses the standard library only. Checks both the original E0425/E0107 family
and the per-thread COM initialization contract for cached Media Foundation APIs.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MFT = (ROOT / 'crates/platform/src/media_foundation/mft.rs').read_text(encoding='utf-8')
MOD = (ROOT / 'crates/platform/src/media_foundation/mod.rs').read_text(encoding='utf-8')
ADAPTERS = (ROOT / 'crates/platform/src/gpu_adapters.rs').read_text(encoding='utf-8')
BUILD = (ROOT / 'scripts/build-win.ps1').read_text(encoding='utf-8')


def api_is_thread_safe_on_lookup(source):
    # Limit the check to the body of api(), not load(), so an initialization
    # made only by the first thread does not incorrectly pass the test.
    begin = source.find('pub fn api() ->')
    end = source.find('\nfn load()', begin)
    if begin < 0 or end < 0:
        return False
    body = source[begin:end]
    init = body.find('ensure_com()?;')
    lookup = body.find('API.get_or_init(load)')
    return 0 <= init < lookup


def type_contract_is_string_error(mod, adapters):
    explicit_std_result = re.search(
        r'pub fn h264_hardware_encoder_candidates\(\)\s*->\s*'
        r'std::result::Result<Vec<String>,\s*String>', mod
    )
    once_lock = 'H264_MFT_ENCODERS: OnceLock<Result<Vec<String>, String>>' in adapters
    return bool(explicit_std_result and once_lock)


class BuildFix2Tests(unittest.TestCase):
    def test_com_initializes_for_every_api_caller(self):
        self.assertTrue(api_is_thread_safe_on_lookup(MFT))

    def test_guard_inside_load_only_is_insufficient(self):
        without_api_guard = MFT.replace('    ensure_com()?;\n    static API:', '    static API:', 1)
        self.assertFalse(api_is_thread_safe_on_lookup(without_api_guard))

    def test_guard_after_cache_lookup_is_too_late(self):
        late = MFT.replace(
            '    ensure_com()?;\n    static API:', '    static API:', 1
        ).replace(
            '    API.get_or_init(load).as_ref().map_err(Clone::clone)',
            '    API.get_or_init(load).as_ref().map_err(Clone::clone)\n    ensure_com()?;', 1
        )
        self.assertFalse(api_is_thread_safe_on_lookup(late))

    def test_h264_output_guid_is_imported_and_not_nv12(self):
        imports = MFT.split('};', 1)[0]
        self.assertIn('MFVideoFormat_H264', imports)
        self.assertRegex(MFT, r'guidSubtype:\s*MFVideoFormat_H264\b')

    def test_gpu_diagnostic_result_types_agree(self):
        self.assertTrue(type_contract_is_string_error(MOD, ADAPTERS))
        broken = MOD.replace('std::result::Result<Vec<String>, String>', 'Result<Vec<String>, String>', 1)
        self.assertFalse(type_contract_is_string_error(broken, ADAPTERS))

    def test_windows_test_script_checks_platform_before_long_tests(self):
        pos_check = BUILD.find("Invoke-Cargo -Arguments @('check','--locked','-p','filmcraft-platform')")
        pos_test = BUILD.find("Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_')")
        self.assertGreaterEqual(pos_check, 0)
        self.assertLess(pos_check, pos_test)
        self.assertIn("Invoke-Cargo -Arguments @('check','--locked','-p','filmcraft-ui-egui')", BUILD)
        self.assertIn('scripts/test_mf_buildfix2.py', BUILD)


if __name__ == '__main__':
    unittest.main(verbosity=2)
