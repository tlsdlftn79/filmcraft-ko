#!/usr/bin/env python3
"""RC22: static checks only. Native browser and IME must still be tested on Windows."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent.parent
read = lambda p: (ROOT / p).read_text(encoding="utf-8")
link = read("crates/ui-egui/src/links.rs")
head = read("crates/ui-egui/src/header.rs")
menu = read("crates/ui-egui/src/menus.rs")
dialog = read("crates/ui-egui/src/panels/dialogs.rs")
gfx = read("crates/ui-egui/src/panels/graphics.rs")
assert 'pub fn open(ctx: &egui::Context, url: &str) -> Result<(), String>' in link
assert 'ctx.copy_text(url.to_owned())' in link
assert 'std::process::Command::new("explorer.exe")' in link
assert 'std::process::Command::new("rundll32.exe")' in link
assert 'windows_default_browser_has_a_fallback_command' in link
assert 'Browser launch requested' in head and 'Browser launch failed' in head
assert 'Browser launch requested' in menu and 'Browser launch failed' in dialog
assert 'discord_fits && donate_r.min.x > left_end + 20.0' in head
assert 'let drag = ui.interact(drag_rect,' in head
assert gfx.count('begin_native_text_ime(ui,') >= 2
assert 'should_interrupt_composition: false' in gfx
assert 'should_resume_text_focus(' in gfx and 'acquire_text_focus(' in gfx
assert 'ime_consumes_key_at(' in gfx and 'ImeFrameEchoBudget::new(&events)' in gfx
assert 'ImeEvent::Disabled' not in gfx
assert 'https://ctee.kr/place/caw' in link
assert 'https://discord.gg/artcraft' in link
assert 'Browser launch failed; URL copied to clipboard' in read('crates/ui-egui/src/i18n/ko.tsv')
assert re.search(r'^#define PatchChannel "Stable"$',read('packaging/windows/filmcraft-korean.iss'),re.M)
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
print('[OK] RC22 buttons, browser fallback, IME routing and release identity; static only')
