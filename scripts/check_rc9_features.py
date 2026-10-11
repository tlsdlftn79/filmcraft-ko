#!/usr/bin/env python3
"""Source contracts only: this is NOT a Rust compiler / GPU / IME runtime test."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
def read(name): return (ROOT/name).read_text(encoding='utf-8')
graphics = read('crates/ui-egui/src/panels/graphics.rs')
adapters = read('crates/platform/src/gpu_adapters.rs')
ui = read('crates/ui-egui/src/panels/export_mode.rs')
host = read('crates/ui-egui/src/lib.rs')
main = read('apps/filmcraft/src/main.rs')
assert 'fn unrelated_latin_text_survives_hangul_preedit()' in graphics
assert 'fn matching_preedit_echo_is_not_persisted()' in graphics
assert 'fn empty_preedit_does_not_eat_following_keys()' in graphics
assert '!committed && !dismissed && !ed.ime_preedit.is_empty() && incoming == ed.ime_preedit' in graphics
assert 'pub fn warm_probe()' in adapters and 'CreateDXGIFactory1()' in adapters
assert '0x1002' in adapters and '0x8086' in adapters and '0x10de' in adapters
assert 'gpu_adapters: Option<Box<dyn Fn() -> Option<Vec<(String, String)>>>>' in host
assert 'filmcraft_platform::gpu_adapters::warm_probe()' in main
assert 'Detected graphics adapter: {name} ({vendor})' in ui
assert 'Native in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.' in ui
assert re.search(r'(?m)^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'))
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
for language in ['ko', 'es', 'ja', 'pt-br', 'uk', 'zh-cn']:
    catalog = read(f'crates/ui-egui/src/i18n/{language}.tsv')
    for key in ['Detected graphics adapter: {name} ({vendor})','Detecting graphics adapters...']:
        assert f'\t{key}\t' in catalog, (language, key)
print('[PASS] RC10 IME event filtering, DXGI vendor diagnostics, i18n, installer and release metadata.')
print('[NOTE] AMF/QSV now use FilmCraft-managed FFmpeg transcoding, not native encoder factories. No Windows build was run.')
