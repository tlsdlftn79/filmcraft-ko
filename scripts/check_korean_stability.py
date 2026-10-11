#!/usr/bin/env python3
"""Static checks for the v0.6.0 RC4 Unicode/IME and Korean-caption patch.

This is not a replacement for the Rust unit tests or a Windows IME test.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, needles: list[str]) -> list[str]:
    file = ROOT / path
    if not file.is_file():
        return [f"{path}: file is missing"]
    source = file.read_text(encoding="utf-8-sig")
    return [f"{path}: expected {needle!r}" for needle in needles if needle not in source]


def main() -> int:
    checks = {
        "crates/ui-egui/src/panels/graphics.rs": [
            "UnicodeSegmentation::grapheme_indices", "fn floor_boundary(",
            "fn prev_scalar(", "fn next_scalar(",
            "fn has_ime_edit(", "fn text_is_ime_echo(", "fn apply_ime_or_text(",
            "korean_ime_commit_preserves_unrelated_text_same_frame",
            "korean_ime_dismissal_does_not_drop_latin_input",
            "korean_word_navigation_keeps_grapheme_boundaries",
            "korean_ime_commit_deduplicates_text_in_both_event_orders",
            "korean_grapheme_deletion_never_splits_jamo_or_emoji",
            "korean_ime_selection_with_malformed_byte_offsets_is_clamped",
            "korean_ime_dismissal_frame_preserves_fresh_text_in_either_order",
            "korean_ime_surrounding_deletion_counts_scalars_as_required",
            "korean_ime_blank_preedit_ends_composition_without_committing",
            "korean_ime_blank_preedit_does_not_swallow_keyboard_text",
            "fn ime_consumes_editor_keys(",
            "korean_ime_dismissal_prevents_double_enter_backspace_and_escape",
        ],
        "crates/ui-egui/Cargo.toml": ['unicode-segmentation = "1.13"'],
        "Cargo.lock": ['name = "filmcraft-ui-egui"', ' "unicode-segmentation",'],
        "crates/captions/src/burn.rs": [
            "use unicode_segmentation::UnicodeSegmentation;",
            "word.graphemes(true)", "korean_unspaced_captions_wrap_inside_frame",
            "korean_grapheme_wrap_preserves_jamo_and_emoji",
            "korean_selected_caption_font_is_not_ignored",
            "korean_caption_outline_and_background_fit_frame",
            "korean_caption_very_long_text_uses_bounded_overlay",
        ],
        "crates/captions/Cargo.toml": ['unicode-segmentation = "1.13"', 'encoding_rs = "0.8.42"'],
        "crates/captions/src/lib.rs": ['pub fn decode_srt_text(', 'encoding_rs::EUC_KR.decode(bytes)'],
        "crates/render/src/graphic_clip.rs": ['fn korean_text_layer_font_and_graphemes_survive_layout()'],
        "crates/captions/tests/korean_roundtrip.rs": [
            "fn korean_caption_roundtrip_srt_and_webvtt()",
            "fn korean_caption_bom_and_crlf_import()",
            "fn korean_cp949_legacy_srt_import_and_utf8_export()",
            "fn korean_srt_unicode_bom_precedes_legacy_decoder()",
            "Format::Srt", "Format::WebVtt", "안녕하세요!",
        ],
        "scripts/build-win.ps1": [
            "'filmcraft-captions','korean_'",
            "'scripts/check_korean_stability.py'",
        ],
        "packaging/windows/filmcraft-korean.iss": [
            '#define PatchVersion "0.6.0"',
            "PrivilegesRequired=lowest",
        ],
    }
    errors = [err for file, needles in checks.items() for err in require(file, needles)]
    if errors:
        for error in errors:
            print("[FAIL]", error)
        return 1
    graphics = (ROOT / "crates/ui-egui/src/panels/graphics.rs").read_text(encoding="utf-8")
    if "ImeEvent::Disabled" in graphics or "ImeEvent::Enabled" in graphics:
        print("[FAIL] Deprecated egui IME variants still used in graphics.rs")
        return 1
    print("[OK] Korean IME selective deduplication, Unicode word navigation, CJK caption wrap, and installer hooks exist")
    print("[NOTE] Structural checks only; Rust compile and Windows IME/export tests must be run on Windows")
    return 0


if __name__ == '__main__':
    sys.exit(main())
