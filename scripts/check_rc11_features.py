#!/usr/bin/env python3
"""RC12 static source contract. Runtime claims require separate Windows validation."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
read = lambda path: (ROOT / path).read_text(encoding='utf-8')
gfx = read('crates/ui-egui/src/panels/graphics.rs')
build = read('scripts/build-win.ps1')
probe = read('scripts/probe_h264_gpu.py')
platform = read('crates/platform/src/lib.rs')
assert 'fn focus_new_text_session(ui: &egui::Ui, edit: &mut GfxEdit)' in gfx
assert 'focus_new_text_session(ui, &mut edit);' in gfx
assert gfx.count('focus_new_text_session(ui, &mut edit);') == 2
assert 'ui.ctx().request_repaint();' in gfx
assert 'acquire_text_focus(memory, id, &mut edit.focus_initialized)' in gfx
assert 'fn korean_commit_and_unrelated_latin_echo_stay_distinct()' in gfx
assert 'fn new_edit_focus_is_one_shot_and_never_steals_property_edit_focus()' in gfx
assert 'ImeEvent::Disabled' not in gfx
assert 'probe_h264_gpu.py' in build
assert "korean_ime_rc11_first_focus_tests" in build
assert '--self-test' in build
assert '--require' in probe and '--encoder' in probe and '--json' in probe
for encoder in ('h264_amf', 'h264_qsv', 'h264_nvenc'):
    assert encoder in probe
assert 'TemporaryDirectory' in probe and 'check_stream' in probe
assert 'filmcraft_export::register_encoder(nvenc::export::factory)' in platform
assert 'register_encoder(media_foundation' not in platform
assert 'register_encoder(amd' not in platform
assert re.search(r'^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'), re.M)
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
assert 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe' in read('scripts/build-installer.ps1')
assert 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip' in build
print('[PASS] RC12 one-shot text editor focus, native IME event tests, opt-in GPU smoke diagnostics, safe encoder registration and packaging')
print('[LIMIT] AMD AMF/Intel QSV FilmCraft export, Rust build and Windows native IME not verified.')
