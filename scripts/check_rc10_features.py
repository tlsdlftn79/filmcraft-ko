#!/usr/bin/env python3
"""RC10 source contract tests: static only, not an H.264 hardware encode test."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
read = lambda p: (root/p).read_text(encoding='utf-8')
mft = read('crates/platform/src/media_foundation/mft.rs')
platform = read('crates/platform/src/media_foundation/mod.rs')
adapters = read('crates/platform/src/gpu_adapters.rs')
ui = read('crates/ui-egui/src/panels/export_mode.rs')
host = read('crates/ui-egui/src/lib.rs')
main = read('apps/filmcraft/src/main.rs')
assert 'MFT_CATEGORY_VIDEO_ENCODER' in mft
assert 'MFT_ENUM_FLAG_HARDWARE' in mft
assert 'MFT_ENUM_FLAG_SORTANDFILTER' in mft
assert re.search(r'self.transforms\(MFT_CATEGORY_VIDEO_ENCODER, flags, None, Some\(output\)\)', mft)
assert 'guidSubtype: MFVideoFormat_H264' in mft
assert 'pub fn h264_hardware_encoder_candidates()' in platform
assert 'h264_hardware_encoder_names()' in platform
assert 'pub fn warm_h264_encoder_probe()' in adapters
assert 'H264_MFT_ENCODERS: OnceLock<Result<Vec<String>, String>>' in adapters
assert 'gpu_h264_encoder_candidates: Option<Box<dyn Fn() -> Option<Result<Vec<String>, String>>>>' in host
assert 'warm_h264_encoder_probe();' in main
assert 'Hardware H.264 encoder candidate (not enabled for export): {name}' in ui
assert 'Native in-process H.264: NVENC. AMD/Intel use FilmCraft-managed FFmpeg conversion.' in ui
# Enumeration must never be confused with registering an encoder factory.
assert 'register_encoder' not in adapters
assert re.search(r'^#define PatchChannel "Stable"$', read('packaging/windows/filmcraft-korean.iss'), re.M)
assert "VERSION = '0.6.0_Stable'" in read('scripts/verify_release.py')
for lang in ('ko','es','ja','pt-br','uk','zh-cn'):
    catalog=read('crates/ui-egui/src/i18n/'+lang+'.tsv')
    for key in ('Checking Windows hardware H.264 encoder candidates...',
                'No registered Windows hardware H.264 encoder candidates found.',
                'Hardware H.264 encoder candidate (not enabled for export): {name}',
                'Windows hardware H.264 encoder discovery unavailable.'):
        assert '\t'+key+'\t' in catalog,(lang,key)
print('[PASS] RC10 MF H.264 encoder-candidate integration, nonblocking UI, export safety and release metadata')
print('[LIMIT] MFT enumeration is not AMD AMF or Intel QSV encoding; requires Windows runtime validation.')
