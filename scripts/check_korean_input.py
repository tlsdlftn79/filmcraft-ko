#!/usr/bin/env python3
"""Static contract for Korean IME patch. Real IME behavior requires Windows tests."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
checks = {
    'crates/ui-egui/src/panels/graphics.rs': [
        'fn apply_ime_or_text(', 'egui::Event::Ime(ime) => Some(handle_ime(text, ed, ime))',
        'egui::ImeEvent::Preedit { text: candidate, .. }',
        'egui::ImeEvent::Commit(committed)', 'egui::ImeEvent::DeleteSurrounding',
        'text_is_ime_echo(s, ed, frame)',
        'insert_committed_text', 'korean_preedit_does_not_save_partial_syllables',
        'utf8_selection_and_ime_cancel_are_safe',
        'fn ime_consumes_editor_keys(',
        'korean_ime_dismissal_prevents_double_enter_backspace_and_escape',
        'korean_ime_blank_preedit_ends_composition_without_committing',
        'korean_ime_commit_preserves_unrelated_text_same_frame',
        'id(egui::Id::new(("gfx-source-text", clip.0, l)))',
    ],
    'crates/ui-egui/src/state.rs': ['#[serde(skip)]', 'pub ime_preedit: String'],
    'crates/text/src/fonts.rs': ['fn korean_fallback(c: char)', 'scan_system();', 'fn hangul_uses_available_korean_font_in_english_ui()'],
    'crates/engine/src/graphics_tests.rs': ['fn hangul_graphics_text_roundtrip_and_undo()'],
    'scripts/build-win.ps1': ['check_korean_input.py', "'filmcraft-text','hangul_'", "'filmcraft-engine','hangul_graphics_'"],
}
for path, needles in checks.items():
    content = (ROOT/path).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in content:
            raise SystemExit(f'[FAIL] {path}: missing {needle}')
graphics = (ROOT/'crates/ui-egui/src/panels/graphics.rs').read_text(encoding='utf-8')
if 'ImeEvent::Disabled' in graphics or 'ImeEvent::Enabled' in graphics:
    raise SystemExit('[FAIL] Deprecated egui IME variant found')
print('[OK] Korean IME Preedit/Commit, empty-Preedit dismissal and test hooks found')
print('[NOTE] Static check only: actual Windows IME composition and final Rust build unverified.')
