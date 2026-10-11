#!/usr/bin/env python3
"""Validate artifacts created on Windows, without pretending to execute them.

Run AFTER PACKAGE.cmd and INSTALL.cmd. This checks names, lengths, contents,
checksums and executable headers; it does not prove an installation or video export.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import argparse
import hashlib
from pathlib import Path
import re
import sys
from zipfile import ZipFile, BadZipFile

VERSION = '0.6.0_Stable'
REQUIRED_PORTABLE = {'filmcraft.exe', 'filmcraft-cli.exe', 'portable.txt',
                     'README-KOREAN.md', 'CHANGELOG-KO.md', 'STABLE_RELEASE_GATE_KO.md', 'LICENSE-MIT', 'LICENSE-APACHE'}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify_checksum(path: Path) -> None:
    checksum = Path(str(path) + '.sha256')
    if not checksum.is_file():
        raise ValueError(f'Missing SHA-256 companion: {checksum}')
    # Support the standard sha256sum format (hash + two spaces + filename).
    contents = checksum.read_text(encoding='ascii').strip()
    m = re.fullmatch(r'([a-fA-F0-9]{64})  ([^\\/\r\n]+)', contents)
    if not m:
        raise ValueError(f'Invalid checksum file: {checksum}')
    if m.group(2) != path.name:
        raise ValueError(f'Checksum names wrong output: {path.name}')
    if m.group(1).lower() != sha256(path):
        raise ValueError(f'SHA-256 mismatch: {path.name}')


def verify_portable(path: Path) -> None:
    verify_checksum(path)
    try:
        with ZipFile(path) as zip_file:
            files = {n for n in zip_file.namelist() if not n.endswith('/')}
            if files != REQUIRED_PORTABLE:
                raise ValueError(f'Unexpected portable payload: missing={REQUIRED_PORTABLE - files}; extra={files - REQUIRED_PORTABLE}')
            corrupt = zip_file.testzip()
            if corrupt is not None:
                raise ValueError(f'Bad ZIP entry: {corrupt}')
            for name in ('filmcraft.exe', 'filmcraft-cli.exe'):
                with zip_file.open(name) as f:
                    if f.read(2) != b'MZ':
                        raise ValueError(f'{name} lacks MZ executable magic')
    except BadZipFile as exc:
        raise ValueError(f'Invalid ZIP: {exc}') from exc


def verify_installer(path: Path) -> None:
    verify_checksum(path)
    if path.stat().st_size < 4096:
        raise ValueError(f'Installer EXE is too small: {path}')
    with path.open('rb') as f:
        if f.read(2) != b'MZ':
            raise ValueError(f'Installer missing MZ executable header: {path}')


def verify(dist: Path) -> list[str]:
    if not dist.is_dir():
        raise ValueError(f'Build output directory not found: {dist}')
    portable = dist / f'FilmCraft_v{VERSION}_Korean_Windows_x64_Portable.zip'
    installer = dist / f'FilmCraft_v{VERSION}_Korean_Windows_x64_Setup.exe'
    if not portable.is_file() or not installer.is_file():
        raise ValueError(f'Both installer and portable artifacts required: {dist}')
    verify_portable(portable)
    verify_installer(installer)
    return [portable.name, installer.name]


def build_manifest(dist: Path, files: list[str]) -> dict:
    """Describe SHA-checked Windows artifacts; no unrun runtime tests inferred."""
    return {
        'schema_version': 1,
        'release': VERSION,
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'windows_runtime_verified': False,
        'verification_scope': 'ZIP entries, PE MZ headers, sidecar SHA-256 and file sizes only',
        'artifacts': [
            {'filename': name, 'size_bytes': (dist/name).stat().st_size, 'sha256': sha256(dist/name)}
            for name in files
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', type=Path, default=Path(__file__).resolve().parents[1] / 'dist')
    parser.add_argument('--manifest', type=Path, help='Write artifact-level JSON manifest after successful validation')
    args = parser.parse_args()
    try:
        from check_stable_release import validate
        validate()
        files = verify(args.dist)
    except (ValueError, OSError) as exc:
        print(f'[FAIL] {exc}', file=sys.stderr)
        return 1
    if args.manifest is not None:
        manifest = build_manifest(args.dist, files)
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(f'[OK] Wrote artifact manifest: {args.manifest}')
    for name in files:
        print(f'[OK] Checked payload and SHA-256: {name}')
    print('[NOTE] Artifact checks do not replace Windows installation, IME, or MP4 export testing.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
