#!/usr/bin/env python3
"""RC8 source integration checks. Does NOT claim real GPU or Windows execution."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
read = lambda p: (root / p).read_text(encoding='utf-8')
platform = read('crates/platform/src/nvenc/mod.rs')
frontend = read('crates/ui-egui/src/panels/export_mode.rs')
host = read('crates/ui-egui/src/lib.rs')
main = read('apps/filmcraft/src/main.rs')
installer = read('packaging/windows/filmcraft-korean.iss')
assert 'pub fn warm_h264_probe()' in platform
assert 'pub fn h264_probe_result() -> Option<bool>' in platform
assert 'std::thread::Builder::new().name("nvenc-h264-probe"' in platform
assert 'h264_nvenc_available: Option<Box<dyn Fn() -> Option<bool>>>' in host
assert 'filmcraft_platform::nvenc::warm_h264_probe();' in main
assert 'NvencStatus::Checking' in frontend
assert 'nvenc_status(detected)' in frontend
assert 'Quick Export failed: {reason}' in frontend
assert 'fn korean_filename_survives_gpu_setting_changes()' in frontend
assert 'Native in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.' in frontend
assert '#define PatchChannel "Stable"' in installer
for lang in ('ko','es','ja','pt-br','uk','zh-cn'):
    catalog = read(f'crates/ui-egui/src/i18n/{lang}.tsv')
    for key in ('NVIDIA NVENC unavailable: GPU Auto will use CPU encoding.', 'Quick Export failed: {reason}'):
        assert f'\t{key}\t' in catalog, (lang,key)
print('[OK] RC8 asynchronous NVENC status, CPU fallback messaging, Unicode filename and installer version checks')
print('[NOTE] Actual NVIDIA/AMD/Intel GPU hardware runs and Windows builds are NOT tested here.')
