#!/usr/bin/env python3
"""RC12 static source contract: not a substitute for Windows IME or GPU tests."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
read = lambda name: (ROOT/name).read_text(encoding='utf-8')
gfx = read('crates/ui-egui/src/panels/graphics.rs')
probe = read('scripts/probe_h264_gpu.py')
build = read('scripts/build-win.ps1')
platform = read('crates/platform/src/lib.rs')
assert 'FILMCRAFT_IME_DIAGNOSTICS' in gfx
assert 'fn trace_native_ime(' in gfx and 'fn ime_diagnostic_event(' in gfx
assert 'trace_native_ime(false,' in gfx and 'trace_native_ime(true,' in gfx
assert 'fn korean_diagnostics_never_expose_input_content()' in gfx
assert 'fn korean_ime_delete_surrounding_recovers_non_scalar_caret()' in gfx
assert 'while begin > 0 && !text.is_char_boundary(begin)' in gfx
assert 'eprintln!("[FILMCRAFT-IME] focused=' in gfx
assert 'FILMCRAFT_IME_DIAGNOSTICS=1' in gfx
assert 'text.chars().count()' in gfx
assert 'DeleteSurrounding' in gfx and 'ImeEvent::Disabled' not in gfx
assert "'-count_frames'" in probe and "'nb_read_frames'" in probe
assert "'-xerror'" in probe and "'decode-failed'" in probe
assert 'decoded frames' in probe
assert 'scripts/check_rc12_features.py' in build
assert 'register_encoder(media_foundation' not in platform
assert 'register_encoder(amd' not in platform
assert 'register_encoder(nvenc::export::factory)' in platform
assert re.search(r'^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'), re.M)
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
assert 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe' in read('scripts/build-installer.ps1')
assert 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip' in build
print('[PASS] RC12 IME opt-in privacy-safe diagnostics, UTF-8 recovery, decoded-video GPU probe and release metadata')
print('[LIMIT] AMD/Intel FilmCraft encoder integration, native IME, Rust MSVC build and setup execution remain unverified.')
