#!/usr/bin/env python3
"""RC22 native external-link dispatch and hit-target regression checks.

Static checks only: does not spawn a browser or claim tested Windows clicks.
"""
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parent.parent
read = lambda name: (ROOT / name).read_text(encoding='utf-8')
links = read('crates/ui-egui/src/links.rs')
header = read('crates/ui-egui/src/header.rs')
menus = read('crates/ui-egui/src/menus.rs')
about = read('crates/ui-egui/src/panels/dialogs.rs')
toml = tomllib.loads(read('crates/ui-egui/Cargo.toml'))
assert toml['dependencies']['eframe']['workspace'] is True
# Desktop eframe is built with default features disabled and no links flag;
# egui::Context::open_url alone would therefore be ignored on Windows.
assert 'default-features = false' in read('Cargo.toml')
assert 'native_browser_commands(url)' in links
assert 'Command::new("rundll32.exe")' in links
assert 'Command::new("explorer.exe")' in links
assert 'fallback.arg("url.dll,FileProtocolHandler").arg(url)' in links
assert 'Command::new("open")' in links
assert 'Command::new("xdg-open")' in links
assert 'cmd.arg(url)' in links or 'explorer.arg(url)' in links
assert 'ctx.copy_text(url.to_owned())' in links
assert 'pub fn open(ctx: &egui::Context, url: &str) -> Result<(), String>' in links  # Error fallback
assert '#[cfg(target_arch = "wasm32")]' in links and 'ctx.open_url(egui::OpenUrl::new_tab(url))' in links
assert 'if !url.starts_with("https://")' in links
assert 'https://ctee.kr/place/caw' in links
assert 'https://discord.gg/artcraft' in links
assert 'crate::links::open(ui.ctx(), crate::links::DISCORD)' in header
assert 'crate::links::open(ui.ctx(), crate::links::KOREAN_PATCH_SUPPORT)' in header
assert 'let drag = ui.interact(rect,' not in header
assert 'let drag = ui.interact(drag_rect,' in header
assert header.index('let drag_rect =') > header.index('let donate_r =')
assert 'header.discord' in header and 'header.supportKorean' in header
assert 'links::open(ui.ctx(), url)' in about
assert 'crate::links::open(ctx, url)' in menus
assert 'RC22' in read('scripts/build-win.ps1')
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
assert re.search(r'^#define PatchChannel "Stable"$',read('packaging/windows/filmcraft-korean.iss'),re.M)
assert 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe' in read('scripts/build-installer.ps1')
print('[OK] RC22: native Windows/macOS/Linux external-link launcher, safe header hit regions, release identity')
print('[LIMIT] Rust compiler and Windows interactive clicks have not been exercised by this static test')
