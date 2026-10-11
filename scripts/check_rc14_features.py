#!/usr/bin/env python3
"""RC14 source release guards (actual Rust/Windows operation remains unverified)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
read = lambda relative: (ROOT / relative).read_text(encoding='utf-8')
editor = read('crates/ui-egui/src/panels/graphics.rs')
assert 'let navigation_layout = if changed {' in editor
assert 'pending.text.clone_from(&text);' in editor
assert 'navigation_layout.lines[navigation_layout.caret(ed.caret).2].range.end' in editor
assert 'navigation_layout.lines.len()' in editor
assert 'mod korean_rc14_selection_tests' in editor
assert 'fn grapheme_navigation_does_not_split_combining_jamo_or_emoji()' in editor
assert 'ImeEvent::Disabled' not in editor

tool = read('scripts/gpu_mp4_transcode.py')
for api in ('h264_amf', 'h264_qsv', 'h264_nvenc', 'libx264',
            'verify_encoded(', 'stream_types(', 'os.replace(tmp, dst)',
            'if dst.exists():', "if src == dst:", "'-map', '0:s?'", "'-c:s', 'mov_text'"):
    assert api in tool, f'Missing independent GPU conversion contract: {api}'
assert 'register_encoder' not in tool  # no unsupported claim of in-process AMF/QSV
build = read('scripts/build-win.ps1')
assert "scripts/test_rc14_gpu_transcode.py" in build
print('[OK] RC14 Unicode navigation and optional GPU post-export bridge retained')
print('[LIMIT] FFmpeg postprocess is NOT an internal AMD/Intel VideoEncoder implementation')
