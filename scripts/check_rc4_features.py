#!/usr/bin/env python3
"""RC4 feature checks: source contracts, not a replacement for cargo or real Windows UI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def test_native_focus():
    src = read('crates/ui-egui/src/panels/graphics.rs')
    state = read('crates/ui-egui/src/state.rs')
    assert 'pub focus_initialized: bool,' in state
    assert 'if !*initialized {' in src and 'memory.request_focus(id);' in src
    assert 'fn korean_composition_keeps_focus_and_other_widgets_can_take_it()' in src
    assert 'if !ui.memory(|m| m.has_focus(eid)) {' in src
    assert 'if ui.memory(|m| m.has_focus(egui::Id::new(TEXT_EDIT_ID))) {' in src
    assert 'ImeEvent::Disabled' not in src

def test_shorts():
    src = read('crates/export/src/presets.rs')
    assert '"YouTube Shorts 1080×1920 (9:16)"' in src
    assert 'h264(Some((1080, 1920)), 12_000, 16_000)' in src
    assert 'scaling: Scaling::ScaleToFill' in src
    tests = read('crates/engine/src/export_tests.rs')
    assert 'fn youtube_shorts_quick_preset_resolves_vertical_mp4_and_gpu_overrides()' in tests

def test_gpu_wiring():
    ui = read('crates/ui-egui/src/panels/export_mode.rs')
    assert 'quickExport.encoder.cpu' in ui and 'quickExport.encoder.gpu' in ui
    assert '"hardwareEncoding": hardware' in ui and '"gpuRendering": app.ui.export.quick_gpu_rendering' in ui
    assert 'HardwareEncoding::Auto' in ui
    # Check the stable installer channel without changing the original RC4 behavior checks.
    import re
    assert re.search(r'(?m)^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'))

if __name__ == '__main__':
    for test in (test_native_focus, test_shorts, test_gpu_wiring):
        test()
        print('[OK]', test.__name__)
    print('[NOTE] Rust compilation, actual Windows IME, and NVENC acceleration NOT verified')
