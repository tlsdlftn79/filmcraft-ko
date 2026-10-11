#!/usr/bin/env python3
"""RC22 warning regression guard (source check, not a Rust compile)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "crates/ui-egui/src/panels/graphics.rs").read_text(encoding="utf-8")
assert len(re.findall(r"\bfn has_ime_edit\(", source)) == 1
assert re.search(r"(?s)#\[cfg\(test\)\]\s*mod korean_ime_tests \{.*?fn has_ime_edit\(", source), (
    "IME helpers must be inside the unit-test module, not library scope"
)
assert "fn ime_consumes_editor_keys(" in source
assert "#[allow(dead_code)]" not in source, "Do not suppress dead code warnings globally"
assert source.count("has_ime_edit(") >= 5, "Keep existing IME unit tests using the helper"
assert "fn ime_consumes_key_at(" in source, "Keep active production IME key routing"
assert "#[cfg(test)]\nmod korean_ime_tests" in source

release = (ROOT / "scripts/verify_release.py").read_text(encoding="utf-8")
installer = (ROOT / "packaging/windows/filmcraft-korean.iss").read_text(encoding="utf-8")
assert "VERSION = '0.6.0_Stable'" in release
assert '#define PatchChannel "Stable"' in installer
print("[OK] RC22: has_ime_edit is test-only, production IME routing and tests preserved")
print("[LIMIT] Static verification only; run cargo check and cargo test on Windows")
