#!/usr/bin/env python3
"""RC14 IME event-routing source checks (not a substitute for Windows IME testing)."""
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "crates/ui-egui/src/panels/graphics.rs"
s = p.read_text(encoding="utf-8")
required = [
    "fn ime_consumes_key_at(",
    "for (event_index, ev) in events.iter().enumerate()",
    "ime_consumes_key_at(&events, event_index, composing_at_frame_start)",
    "fn key_before_commit_is_claimed_but_later_enter_is_not()",
    "fn candidate_arrow_is_claimed_but_normal_arrow_after_commit_is_not()",
    "fn empty_preedit_dismissal_cannot_delete_document()",
    "fn standalone_typing_keys_are_not_claimed_by_later_ime_events()",
]
for required_text in required:
    assert required_text in s, f"Missing RC14 contract: {required_text}"
assert "if ime_keys_consumed || !ed.ime_preedit.is_empty()" not in s
assert "ImeEvent::Disabled" not in s
print("[OK] RC14 IME per-key routing and regression cases present")
print("[NOTE] Rust unit tests and native Windows IME remain to be executed")
