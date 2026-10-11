#!/usr/bin/env python3
"""RC6 donation link integration tests. Static source checks, not browser execution."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ui = ROOT / "crates/ui-egui/src"
links = (ui / "links.rs").read_text(encoding="utf-8")
menus = (ui / "menus.rs").read_text(encoding="utf-8")
header = (ui / "header.rs").read_text(encoding="utf-8")
about = (ui / "panels/dialogs.rs").read_text(encoding="utf-8")

assert 'pub const KOREAN_PATCH_SUPPORT: &str = "https://ctee.kr/place/caw";' in links
assert '("help.supportKorean", "Support the Korean community patch…", KOREAN_PATCH_SUPPORT)' in links
assert 'uic!("help.supportKorean", "Support the Korean community patch…", ["Help"], None)' in menus
assert 'id if crate::links::url_for(id).is_some()' in menus
assert 'crate::links::open(ctx, url)' in menus
assert 'links::KOREAN_PATCH_SUPPORT, false' in about
assert 'header.supportKorean' in header
assert 'crate::links::open(ui.ctx(), crate::links::KOREAN_PATCH_SUPPORT)' in header
assert 'donate_r.min.x > left_end + 20.0' in header
assert 'title_right = donate_r.min.x - 12.0' in header
assert 'title_right' in header
assert links.count('https://ctee.kr/place/caw') == 2, "URL should be declared once and checked in a unit test"

labels = [
    "Support Korean edition",
    "Support the Korean community patch…",
    "Open Korean patch donation page (external site)",
    "Optional support for the unofficial Korean community patch.",
]
for language in ["ko", "es", "ja", "pt-br", "uk", "zh-cn"]:
    rows = (ui / "i18n" / f"{language}.tsv").read_text(encoding="utf-8").splitlines()
    keys = [line.split("\t")[1] for line in rows if line.count("\t") == 2 and not line.startswith("#")]
    for label in labels:
        assert keys.count(label) == 1, (language, label)
assert re.search(r'^#define PatchChannel "Stable"$', (ROOT / "packaging/windows/filmcraft-korean.iss").read_text(encoding="utf-8"), re.M)
for path in [ROOT / "scripts/build-win.ps1", ROOT / "scripts/build-installer.ps1", ROOT / "scripts/verify_release.py"]:
    assert '0.6.0_Stable' in path.read_text(encoding="utf-8"), path
print("[OK] RC6 Korean community support button, Help command, About link, localization, and packaging config")
print("[NOTE] This does not test click behavior or the external donation website.")
