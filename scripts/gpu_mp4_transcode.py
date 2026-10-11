#!/usr/bin/env python3
"""RC14 optional MP4 hardware transcode after FilmCraft export.

This is deliberately NOT a FilmCraft VideoEncoder plug-in. AMD AMF and Intel
Quick Sync still require an in-process encoder/muxer implementation. This
standalone tool exercises real FFmpeg encoders, validates the output video and
only then publishes a new MP4. The original export is never overwritten.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BACKENDS = {
    'amd': 'h264_amf',
    'intel': 'h264_qsv',
    'nvidia': 'h264_nvenc',
    'cpu': 'libx264',
}


def run(args: list[str], *, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout, check=False)


def video_details(ffprobe: str, src: Path) -> dict:
    p = run([ffprobe, '-v', 'error', '-show_entries',
             'stream=index,codec_name,codec_type,width,height:format=duration',
             '-of', 'json', str(src)], timeout=30)
    if p.returncode:
        raise RuntimeError('ffprobe failed: ' + (p.stderr or p.stdout).strip()[-1000:])
    obj = json.loads(p.stdout)
    video = next((s for s in obj.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not video:
        raise RuntimeError('Input/output has no video stream')
    if int(video.get('width', 0)) <= 0 or int(video.get('height', 0)) <= 0:
        raise RuntimeError('Invalid video dimensions')
    return video


def stream_types(ffprobe: str, source: Path) -> list[str]:
    probe = run([ffprobe, '-v', 'error', '-show_entries', 'stream=codec_type',
                 '-of', 'json', str(source)], timeout=30)
    if probe.returncode:
        raise RuntimeError('Could not inspect audio/subtitles: ' + probe.stderr[-800:])
    return [entry.get('codec_type', '') for entry in json.loads(probe.stdout).get('streams', [])]


def available_encoders(ffmpeg: str) -> set[str]:
    result = run([ffmpeg, '-hide_banner', '-encoders'], timeout=30)
    if result.returncode:
        raise RuntimeError('Could not enumerate FFmpeg encoders: ' + result.stderr[-500:])
    # Do not treat a GPU *vendor* as proof of encoder availability. This only
    # checks the binary's codecs; actual device creation is verified by encode.
    return {parts[1] for line in result.stdout.splitlines()
            if len(parts := line.strip().split()) >= 2 and parts[0].startswith('V')}


def candidate_backends(selected: str, available: set[str], allow_cpu_fallback: bool) -> list[str]:
    order = ['nvidia', 'amd', 'intel'] if selected == 'auto' else [selected]
    if allow_cpu_fallback or selected == 'cpu':
        order.append('cpu')
    # An explicit backend should report when it is missing rather than silently
    # using another GPU; auto may try any of the supported backends.
    result = []
    for backend in order:
        if BACKENDS[backend] in available and backend not in result:
            result.append(backend)
    return result


def encode_command(ffmpeg: str, source: Path, dest: Path, backend: str, bitrate: int, shorts: bool) -> list[str]:
    if not 100 <= bitrate <= 100000:
        raise ValueError('bitrate must be 100..100000 kbps')
    command = [ffmpeg, '-hide_banner', '-nostdin', '-loglevel', 'error', '-y', '-i', str(source),
               '-map', '0:v:0', '-map', '0:a?', '-map', '0:s?', '-map_metadata', '0',
               '-c:v', BACKENDS[backend], '-b:v', f'{bitrate}k']
    filters = []
    if shorts:
        # Fill 9:16 with a centre crop, preserving the input frame rate.
        filters += ['scale=1080:1920:force_original_aspect_ratio=increase', 'crop=1080:1920']
    filters.append('format=nv12' if backend == 'intel' else 'format=yuv420p')
    command += ['-vf', ','.join(filters)]
    # Copy AAC audio when present; refuse to silently drop audio. The output
    # validation below verifies that an input audio stream is preserved.
    command += ['-c:a', 'copy', '-c:s', 'mov_text', '-movflags', '+faststart', '-f', 'mp4', str(dest)]
    return command


def verify_encoded(ffmpeg: str, ffprobe: str, source: Path, output: Path, shorts: bool) -> None:
    if not output.exists() or output.stat().st_size < 1024:
        raise RuntimeError('Encoder produced no usable MP4')
    src = video_details(ffprobe, source)
    dst = video_details(ffprobe, output)
    if dst.get('codec_name') != 'h264':
        raise RuntimeError(f"Wrong output codec: {dst.get('codec_name')}")
    expected = (1080, 1920) if shorts else (int(src['width']), int(src['height']))
    if (int(dst['width']), int(dst['height'])) != expected:
        raise RuntimeError('Output dimensions do not match requested mode')
    original_types = stream_types(ffprobe, source)
    output_types = stream_types(ffprobe, output)
    for media_type in ('audio', 'subtitle'):
        if original_types.count(media_type) != output_types.count(media_type):
            raise RuntimeError(f'{media_type} stream count changed during transcode')
    # Actual decode, not merely a playable-looking MP4 header.
    p = run([ffmpeg, '-hide_banner', '-nostdin', '-v', 'error', '-xerror',
             '-i', str(output), '-map', '0:v:0', '-f', 'null', '-'], timeout=900)
    if p.returncode:
        raise RuntimeError('Export fails full video decoding: ' + p.stderr[-1200:])


def transcode(src: Path, dst: Path, selected: str, bitrate: int, shorts: bool,
              allow_cpu_fallback: bool, ffmpeg: str, ffprobe: str) -> str:
    src, dst = src.resolve(), dst.resolve()
    if src == dst:
        raise ValueError('Output must not overwrite the original FilmCraft export')
    if not src.is_file():
        raise FileNotFoundError(src)
    if dst.exists():
        raise FileExistsError(f'Output already exists: {dst}')
    if not dst.parent.is_dir():
        raise FileNotFoundError(f'Output directory does not exist: {dst.parent}')
    video_details(ffprobe, src)
    installed = available_encoders(ffmpeg)
    options = candidate_backends(selected, installed, allow_cpu_fallback)
    if not options:
        raise RuntimeError(f'No requested FFmpeg H.264 encoder found ({selected}); CPU fallback disabled or unavailable')
    errors = []
    for backend in options:
        # Hidden temporary next to final output ensures atomic publication on
        # the same filesystem; a failed GPU attempt is always cleaned up.
        fd, temp_name = tempfile.mkstemp(prefix='.filmcraft-rc14-', suffix='.mp4', dir=dst.parent)
        os.close(fd)
        tmp = Path(temp_name)
        try:
            command = encode_command(ffmpeg, src, tmp, backend, bitrate, shorts)
            print(f'[RC14] Trying {backend} ({BACKENDS[backend]})...', file=sys.stderr)
            proc = run(command)
            if proc.returncode:
                raise RuntimeError(proc.stderr.strip()[-1500:] or f'FFmpeg exit code {proc.returncode}')
            verify_encoded(ffmpeg, ffprobe, src, tmp, shorts)
            # If a hardware codec succeeds but the produced stream cannot be
            # decoded, do not publish it, and do not misreport hardware success.
            os.replace(tmp, dst)
            print(f'[OK] {backend}: {dst}', file=sys.stderr)
            return backend
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            errors.append(f'{backend}: {exc}')
        finally:
            tmp.unlink(missing_ok=True)
    raise RuntimeError('All encoding candidates failed; original retained.\n' + '\n'.join(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Validate post-export H.264 GPU transcode (optional RC14 tool, NOT FilmCraft internal AMF/QSV)')
    parser.add_argument('source', type=Path, help='Existing FilmCraft MP4 input (never modified)')
    parser.add_argument('destination', type=Path, help='New output MP4 (must not exist)')
    parser.add_argument('--encoder', choices=['auto', 'amd', 'intel', 'nvidia', 'cpu'], default='auto')
    parser.add_argument('--bitrate-kbps', type=int, default=12000)
    parser.add_argument('--shorts', action='store_true', help='1080x1920 centre crop; keeps original frame rate')
    parser.add_argument('--allow-cpu-fallback', action='store_true', help='Allow software encoding if GPU attempt fails')
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--ffprobe', default='ffprobe')
    opts = parser.parse_args(argv)
    try:
        for tool in [opts.ffmpeg, opts.ffprobe]:
            if not (shutil.which(tool) or Path(tool).is_file()):
                raise RuntimeError(f'Missing tool: {tool}')
        result = transcode(opts.source, opts.destination, opts.encoder, opts.bitrate_kbps,
                           opts.shorts, opts.allow_cpu_fallback, opts.ffmpeg, opts.ffprobe)
        print(f'Validated encoder: {result}')
        return 0
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f'[ERROR] {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
