#!/usr/bin/env python3
"""RC7 source integration checks, not Windows IME/NVENC runtime verification."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
read = lambda file: (ROOT / file).read_text(encoding='utf-8')
gfx = read('crates/ui-egui/src/panels/graphics.rs')
exp = read('crates/ui-egui/src/panels/export_mode.rs')
win = read('scripts/build-win.ps1')

assert 'should_resume_text_focus(clicked_layer, m.has_focus(eid), ed.focus_initialized)' in gfx
assert 'let clicked_layer = resp.clicked()' in gfx
assert 'm.request_focus(eid);' in gfx
assert 'fn korean_focus_recovery_requires_real_layer_click()' in gfx
assert 'fn korean_multisyllable_commit_swallows_split_echo_once()' in gfx
assert 'fn korean_repeat_after_one_commit_is_not_dropped()' in gfx
assert 'candidate.starts_with(s)' in gfx
assert 'if !s.is_empty()' in gfx
assert 'ImeEvent::Disabled' not in gfx
assert 'Native in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.' in exp
assert 'AMD/Intel H.264 export requires FFmpeg and ffprobe; GPU failures use CPU output.' in exp
assert '"hardwareEncoding": hardware' in exp
assert "FILMCRAFT_TEST_NVENC" in win
assert "--test','nvenc_export" in win
assert "scripts/check_rc7_features.py" in win
for lang in ('ko','es','ja','pt-br','uk','zh-cn'):
    tab = read(f'crates/ui-egui/src/i18n/{lang}.tsv')
    assert 'Native in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.' in exp
    if lang == 'ko':
        assert tab.count('\tNative in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.\t') == 1
assert re.search(r'^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'), re.M)
for f in ('scripts/build-win.ps1', 'scripts/build-installer.ps1', 'scripts/verify_release.py'):
    assert '0.6.0_Stable' in read(f)
print('[OK] RC7 native text focus resume, IME echo budget, current GPU capabilities, Korean translation and packaging contracts')
print('[NOTE] No Rust compilation or Windows GPU/IME runtime test was performed here.')
