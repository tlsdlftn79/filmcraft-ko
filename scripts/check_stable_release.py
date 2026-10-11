#!/usr/bin/env python3
"""Fail closed on v0.6.0 Stable Rust/lockfile/installer/distribution identity.

Runs without cargo; does not claim a successful Windows compilation or GPU test.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.6.0'
CHANNEL = 'Stable'
RELEASE_ID = '0.6.0_Stable'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def version_from_workspace(text):
    section = re.search(r'(?ms)^\[workspace\.package\]\s*\n(.*?)(?=^\[|\Z)', text)
    require(section is not None, 'workspace.package section missing')
    version = re.search(r'(?m)^version\s*=\s*"([^"]+)"', section.group(1))
    require(version is not None, 'workspace.package version missing')
    return version.group(1)


def package_from_manifest(path):
    text = path.read_text(encoding='utf-8')
    section = re.search(r'(?ms)^\[package\]\s*\n(.*?)(?=^\[|\Z)', text)
    require(section is not None, 'missing [package]: '+str(path))
    name = re.search(r'(?m)^name\s*=\s*"([^"]+)"', section.group(1))
    require(name is not None, 'package name missing: '+str(path))
    require('version.workspace = true' in section.group(1), 'package does not inherit workspace version: '+str(path))
    return name.group(1)


def local_lock_versions(text):
    result = {}
    for match in re.finditer(r'(?ms)^\[\[package\]\]\s*\n(.*?)(?=^\[\[package\]\]|\Z)', text):
        part = match.group(1)
        name = re.search(r'(?m)^name\s*=\s*"([^"]+)"', part)
        version = re.search(r'(?m)^version\s*=\s*"([^"]+)"', part)
        require(name is not None and version is not None, 'invalid Cargo.lock package entry')
        if 'source = ' not in part:
            require(name.group(1) not in result,'duplicate local package: '+name.group(1))
            result[name.group(1)] = version.group(1)
    return result


def validate(root=ROOT):
    version = version_from_workspace((root/'Cargo.toml').read_text(encoding='utf-8'))
    require(version==VERSION, f'Rust package version {version} does not match Stable {VERSION}')
    paths = [*sorted((root/'crates').glob('*/Cargo.toml')),
             *sorted((root/'apps').glob('*/Cargo.toml')),root/'xtask/Cargo.toml']
    names={package_from_manifest(p) for p in paths}
    require(len(names)==len(paths), 'duplicate workspace package manifest name')
    versions=local_lock_versions((root/'Cargo.lock').read_text(encoding='utf-8'))
    require(versions.keys()==names, f'Cargo.lock local package list differs: {names ^ versions.keys()}')
    bad={n:v for n,v in versions.items() if v!=VERSION}
    require(not bad, f'Cargo.lock local package version mismatch: {bad}')
    installer=(root/'packaging/windows/filmcraft-korean.iss').read_text(encoding='utf-8')
    require('#define PatchVersion "0.6.0"' in installer,'Inno PatchVersion mismatch')
    require('#define PatchChannel "Stable"' in installer,'Inno channel is not Stable')
    require('AppVersion={#PatchVersion}' in installer, 'Inno stable AppVersion must not be RC suffix')
    require('AppId={{7CC593B6-87C9-4771-B6E9-16BECA9E2F33}' in installer, 'Korean patch upgrade AppId has changed')
    verifier=(root/'scripts/verify_release.py').read_text(encoding='utf-8')
    require("VERSION = '0.6.0_Stable'" in verifier, 'release verifier version mismatch')
    portable='FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip'
    setup='FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe'
    require(portable in (root/'scripts/build-win.ps1').read_text(encoding='utf-8'), 'portable name mismatch')
    require(setup in (root/'scripts/build-installer.ps1').read_text(encoding='utf-8'),'installer name mismatch')
    require(portable in (root/'.github/workflows/korean-windows-rc.yml').read_text(encoding='utf-8'), 'CI portable name mismatch')
    require(setup in (root/'.github/workflows/korean-windows-rc.yml').read_text(encoding='utf-8'), 'CI installer name mismatch')
    win_build = (root/'scripts/build-win.ps1').read_text(encoding='utf-8')
    installer_build = (root/'scripts/build-installer.ps1').read_text(encoding='utf-8')
    stamp = (root/'scripts/stable-build-stamp.ps1').read_text(encoding='utf-8')
    require('Write-StableBuildStamp' in win_build, 'BUILD/PACKAGE does not stamp binaries')
    require('Assert-StableBuildStamp' in installer_build, 'INSTALL -SkipBuild permits stale binaries')
    require('Get-StableSourceFingerprint' in stamp and 'source_sha256' in stamp, 'source fingerprint missing')
    require('Get-FileHash -Algorithm SHA256' in stamp, 'build stamp hash missing')
    verifier = (root/'scripts/verify_release.py').read_text(encoding='utf-8')
    require('windows_runtime_verified' in verifier and 'build_manifest' in verifier,
            'release manifest must not claim Windows runtime testing')
    require('STABLE_RELEASE_GATE_KO.md' in (root/'packaging/windows/filmcraft-korean.iss').read_text(encoding='utf-8'),
            'installer release notes missing')
    print(f'[OK] Stable release identity: Rust {version}, {len(names)} local lock packages, Inno, ZIP, CI')
    print('[NOTE] This is a source-only identity check, not a Windows build or installer run.')
    return len(names)


if __name__=='__main__':
    try:
        validate()
    except (ValueError,OSError) as exc:
        print('[FAIL] '+str(exc))
        raise SystemExit(1)
