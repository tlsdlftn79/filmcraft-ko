#!/usr/bin/env python3
"""RC12 optional hardware-encoder smoke tests (external FFmpeg, NOT FilmCraft export).

Run on Windows with FFmpeg and ffprobe on PATH:
    py -3 scripts/probe_h264_gpu.py --encoder all
    py -3 scripts/probe_h264_gpu.py --encoder intel --require

An FFmpeg encode success is a prerequisite for exploring a FilmCraft backend, not
proof that FilmCraft's Media Foundation packet pipeline can use the encoder.
No downloads are performed and test files are kept only in a temporary folder.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ENCODERS = {"amd": "h264_amf", "intel": "h264_qsv", "nvidia": "h264_nvenc"}


@dataclass(frozen=True)
class ProbeResult:
    vendor: str
    encoder: str
    status: str
    details: str

    def as_dict(self) -> dict[str, str]:
        return dict(vendor=self.vendor, encoder=self.encoder, status=self.status, details=self.details)


def supported_encoder_listing(text: str) -> set[str]:
    """Parse ffmpeg -encoders table without confusing decoders or log chatter."""
    out = set()
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0].startswith('V') and len(parts[0]) >= 6:
            out.add(parts[1])
    return out


def check_stream(info: dict, size: tuple[int, int] = (128, 128)) -> str | None:
    video = [s for s in info.get('streams', []) if s.get('codec_type') == 'video']
    if len(video) != 1:
        return f'expected one video stream, got {len(video)}'
    item = video[0]
    if item.get('codec_name') != 'h264':
        return f'expected H.264, got {item.get("codec_name")}'
    if (item.get('width'), item.get('height')) != size:
        return f'wrong size: {item.get("width")}x{item.get("height")}'
    # Read and count actual decodable frames: a valid container header does not
    # prove the encoder wrote a complete H.264 stream.
    count = item.get('nb_read_frames')
    if count is None or str(count).strip().upper() == 'N/A':
        return 'ffprobe did not report decoded-frame count'
    try:
        frames = int(count)
    except (TypeError, ValueError):
        return f'invalid decoded-frame count: {count!r}'
    if frames != 24:
        return f'expected 24 decodable frames, got {frames}'
    return None


def run_cmd(args: list[str], timeout: int = 45) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(args, capture_output=True, text=True, errors='replace', timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as ex:
        return subprocess.CompletedProcess(args, -1, '', str(ex))


def concise_error(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return ' | '.join(lines[-3:])[:450] or 'encoder did not produce a usable file'


def probe(vendor: str, ffmpeg: str, ffprobe: str, listed: set[str]) -> ProbeResult:
    encoder = ENCODERS[vendor]
    if encoder not in listed:
        return ProbeResult(vendor, encoder, 'not-in-ffmpeg', 'this FFmpeg build lacks the encoder')
    with tempfile.TemporaryDirectory(prefix='filmcraft-rc12-gpu-') as tmp:
        output = Path(tmp) / 'gpu-test.mp4'
        args = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
                '-f', 'lavfi', '-i', 'testsrc2=size=128x128:rate=24:duration=1',
                '-frames:v', '24', '-an', '-pix_fmt', 'nv12',
                '-c:v', encoder, '-b:v', '1000k', '-f', 'mp4', str(output)]
        encoded = run_cmd(args)
        if encoded.returncode != 0:
            return ProbeResult(vendor, encoder, 'encode-failed', concise_error(encoded.stderr))
        if not output.is_file() or output.stat().st_size < 512:
            return ProbeResult(vendor, encoder, 'encode-failed', 'output was missing or empty')
        inspected = run_cmd([ffprobe, '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                             '-show_entries', 'stream=codec_type,codec_name,width,height,nb_read_frames',
                             '-of', 'json', str(output)])
        if inspected.returncode != 0:
            return ProbeResult(vendor, encoder, 'ffprobe-failed', concise_error(inspected.stderr))
        try:
            error = check_stream(json.loads(inspected.stdout))
        except (ValueError, TypeError) as ex:
            error = f'invalid ffprobe JSON: {ex}'
        if error:
            return ProbeResult(vendor, encoder, 'invalid-output', error)
        # Do not report success on a truncated or undecodable MP4. Run a full
        # decoder pass, not only a container-metadata probe.
        decoded = run_cmd([ffmpeg, '-hide_banner', '-nostdin', '-v', 'error',
                           '-xerror', '-i', str(output), '-map', '0:v:0', '-f', 'null', '-'])
        if decoded.returncode != 0:
            return ProbeResult(vendor, encoder, 'decode-failed', concise_error(decoded.stderr))
        return ProbeResult(vendor, encoder, 'smoke-passed', '24 decoded frames, 128x128 H.264 MP4 (FFmpeg only)')


def self_test() -> None:
    listings = ''' V..... h264_amf  AMD AMF H264\n V....D h264_qsv Intel QSV H264\n A..... aac audio\n V..... h264_nvenc NVIDIA NVENC'''
    assert supported_encoder_listing(listings) == set(ENCODERS.values())
    assert supported_encoder_listing(' D..... h264_amf decoder\n A..... aac') == set()
    good = {'codec_type': 'video', 'codec_name': 'h264', 'width': 128, 'height': 128, 'nb_read_frames': '24'}
    assert check_stream({'streams': [good]}) is None
    assert check_stream({'streams': [{**good, 'codec_name': 'hevc'}]}) == 'expected H.264, got hevc'
    assert check_stream({'streams': []}) == 'expected one video stream, got 0'
    assert check_stream({'streams': [{**good, 'width': 1920}]}) == 'wrong size: 1920x128'
    assert check_stream({'streams': [{**good, 'nb_read_frames': '23'}]}) == 'expected 24 decodable frames, got 23'
    assert check_stream({'streams': [{**good, 'nb_read_frames': 'N/A'}]}) == 'ffprobe did not report decoded-frame count'
    assert check_stream({'streams': [{**good, 'nb_read_frames': 'oops'}]}) == "invalid decoded-frame count: 'oops'"
    assert 'driver' in concise_error('first\nMissing driver')
    assert ProbeResult('intel', 'h264_qsv', 'smoke-passed', 'ok').as_dict()['encoder'] == 'h264_qsv'
    print('[PASS] RC12 GPU diagnostic unit tests: 11 (no GPU needed)')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--encoder', choices=['all', *ENCODERS], default='all')
    parser.add_argument('--require', action='store_true', help='return nonzero unless every requested hardware smoke test succeeds')
    parser.add_argument('--json', action='store_true', help='machine-readable JSON results')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:
        print('FFmpeg and ffprobe must be on PATH (no automatic installation).', file=sys.stderr)
        return 2
    encoders = run_cmd([ffmpeg, '-hide_banner', '-encoders'], timeout=15)
    if encoders.returncode != 0:
        print(f'Cannot inspect FFmpeg encoders: {concise_error(encoders.stderr)}', file=sys.stderr)
        return 2
    listing = supported_encoder_listing(encoders.stdout)
    vendors = list(ENCODERS) if args.encoder == 'all' else [args.encoder]
    results = [probe(v, ffmpeg, ffprobe, listing) for v in vendors]
    if args.json:
        print(json.dumps([r.as_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f'{r.vendor}: {r.encoder} = {r.status} ({r.details})')
        print('Note: FFmpeg smoke tests DO NOT enable AMD/Intel export in FilmCraft.')
    return 1 if args.require and any(r.status != 'smoke-passed' for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())
