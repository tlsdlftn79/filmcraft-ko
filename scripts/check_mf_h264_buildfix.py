#!/usr/bin/env python3
"""RC12 BuildFix1 static regression guard. Run from any working directory.

This checks the two documented API/type mismatches; it does NOT replace
cargo check on Windows.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
mft = (ROOT / 'crates/platform/src/media_foundation/mft.rs').read_text(encoding='utf-8')
mod = (ROOT / 'crates/platform/src/media_foundation/mod.rs').read_text(encoding='utf-8')
adapters = (ROOT / 'crates/platform/src/gpu_adapters.rs').read_text(encoding='utf-8')

# Ensure the H.264 encoder filter uses an H.264 subtype and the constant
# is imported from the Windows Media Foundation bindings.
header = mft.split('};', 1)[0]
assert re.search(r'\bMFVideoFormat_H264\b', header), 'H.264 GUID is not imported'
assert re.search(r'guidSubtype:\s*MFVideoFormat_H264\b', mft), 'Encoder output is not H.264'

# The codecs crate exports Result<T> with CodecError, but this diagnostics
# API deliberately reports String to the OnceLock in gpu_adapters.rs.
assert re.search(
    r'fn\s+h264_hardware_encoder_candidates\s*\(\s*\)\s*->\s*'
    r'std::result::Result\s*<\s*Vec\s*<\s*String\s*>\s*,\s*String\s*>',
    mod,
), 'Diagnostics function must return std::result::Result<Vec<String>, String>'
assert 'H264_MFT_ENCODERS: OnceLock<Result<Vec<String>, String>>' in adapters, 'OnceLock error-type contract changed'
print('[OK] RC12 BuildFix1 static API/type checks passed')
