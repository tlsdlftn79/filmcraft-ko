#!/usr/bin/env python3
"""RC22 source-only checks (not a substitute for Rust/Windows tests)."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
gfx=(root/'crates/ui-egui/src/panels/graphics.rs').read_text(encoding='utf8')
engine=(root/'crates/engine/src/export_tools.rs').read_text(encoding='utf8')
ui=(root/'crates/ui-egui/src/panels/export_mode.rs').read_text(encoding='utf8')
gpu=(root/'crates/engine/src/hardware_transcode.rs').read_text(encoding='utf8')
assert 'mod korean_ime_tests {' in gfx
assert 'fn has_ime_edit(' in gfx.split('mod korean_ime_tests {',1)[1]
assert gfx.count('fn has_ime_edit(')==1
assert 'gpuEncoder' in engine and 'spawn_export_gpu' in engine
assert all(e in gpu for e in ['h264_amf','h264_qsv','-xerror','ffprobe','cancel.load','replace_file'])
assert 'quick_gpu_encoder' in ui and 'quickExport.encoder.amd' in ui
print('RC22 source integration checks PASS (Windows build/runtime unverified)')
