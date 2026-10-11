#!/usr/bin/env python3
"""Release artifact verifier unit tests. They run on Linux, macOS or Windows."""
import hashlib
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile
from verify_release import VERSION, REQUIRED_PORTABLE, verify, verify_portable, verify_installer, build_manifest


def fixture(folder: Path):
    portable = folder / f'FilmCraft_v{VERSION}_Korean_Windows_x64_Portable.zip'
    installer = folder / f'FilmCraft_v{VERSION}_Korean_Windows_x64_Setup.exe'
    with ZipFile(portable, 'w') as z:
        for file in REQUIRED_PORTABLE:
            z.writestr(file, b'MZnot-a-real-executable' if file.endswith('.exe') else b'fixture')
    installer.write_bytes(b'MZ' + b'fixture' * 700)
    for path in (portable, installer):
        Path(str(path) + '.sha256').write_text(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n', encoding='ascii')
    return portable, installer


class VerifyReleaseTests(unittest.TestCase):
    def test_valid_file_set_and_checksums(self):
        with tempfile.TemporaryDirectory() as d:
            portable, installer = fixture(Path(d))
            self.assertEqual(len(verify(Path(d))), 2)

    def test_corrupt_sha_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            portable, _ = fixture(Path(d))
            portable.write_bytes(portable.read_bytes() + b'tampered')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                verify_portable(portable)

    def test_wrong_companion_filename_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _, installer = fixture(Path(d))
            sidecar = Path(str(installer) + '.sha256')
            sidecar.write_text('0' * 64 + '  wrong.exe\n', encoding='ascii')
            with self.assertRaisesRegex(ValueError, 'wrong output'):
                verify_installer(installer)

    def test_missing_or_extra_zip_entries_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            portable, _ = fixture(Path(d))
            with ZipFile(portable, 'a') as z:
                z.writestr('surprise.txt', 'extra')
            Path(str(portable) + '.sha256').write_text(
                hashlib.sha256(portable.read_bytes()).hexdigest() + f'  {portable.name}\n', encoding='ascii')
            with self.assertRaisesRegex(ValueError, 'Unexpected portable payload'):
                verify_portable(portable)

    def test_manifest_contains_only_verified_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            fixture(Path(d))
            manifest = build_manifest(Path(d),verify(Path(d)))
            self.assertFalse(manifest['windows_runtime_verified'])
            self.assertEqual(manifest['release'], VERSION)
            self.assertEqual(len(manifest['artifacts']), 2)
            self.assertTrue(all(len(item['sha256'])==64 for item in manifest['artifacts']))

    def test_missing_installer_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _, installer = fixture(Path(d))
            installer.unlink()
            with self.assertRaisesRegex(ValueError, 'Both installer and portable'):
                verify(Path(d))


if __name__ == '__main__':
    unittest.main(verbosity=2)
