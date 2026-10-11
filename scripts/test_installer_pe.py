#!/usr/bin/env python3
"""PE32+ layout regression tests for the shared Windows binary validator.

These are synthetic byte vectors. They exercise an independent Python model of the
PE format and check that the PowerShell release code reads the same field. They do
NOT compile a Rust executable or replace running INSTALL.cmd on Windows.
"""
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/windows-pe.ps1"
INSTALLER = ROOT / "scripts/build-installer.ps1"
BUILDER = ROOT / "scripts/build-win.ps1"


def fake_pe(machine=0x8664, subsystem=2, optional_size=0xF0, magic=0x20B,
            decoy_subsystem=3, file_size=512, pe_offset=0x80):
    """Generate a minimal synthetic PE header with distinct real and decoy values."""
    binary = bytearray(max(file_size, 0x40))
    binary[0:2] = b"MZ"
    struct.pack_into('<i', binary, 0x3C, pe_offset)
    if pe_offset >= 0 and pe_offset + 0x100 <= len(binary):
        binary[pe_offset:pe_offset + 4] = b"PE\x00\x00"
        struct.pack_into('<H', binary, pe_offset + 4, machine)
        struct.pack_into('<H', binary, pe_offset + 0x14, optional_size)
        struct.pack_into('<H', binary, pe_offset + 0x18, magic)
        # Wrong: relative to PE signature. This decoy was mistakenly checked in 0.5.7.
        struct.pack_into('<H', binary, pe_offset + 0x44, decoy_subsystem)
        # Correct: from optional header (PE signature + 4 + COFF header 20).
        struct.pack_into('<H', binary, pe_offset + 0x18 + 0x44, subsystem)
    return bytes(binary)


def valid_pe32_plus(binary, expected_subsystem):
    if len(binary) < 0x40 or binary[:2] != b"MZ":
        return False
    pe = struct.unpack_from('<i', binary, 0x3C)[0]
    if pe < 0x40 or pe > len(binary) - 0x18:
        return False
    if binary[pe:pe + 4] != b"PE\x00\x00":
        return False
    if struct.unpack_from('<H', binary, pe + 4)[0] != 0x8664:
        return False
    optional_size = struct.unpack_from('<H', binary, pe + 0x14)[0]
    if optional_size < 0x46 or pe + 0x18 + optional_size > len(binary):
        return False
    optional_header = pe + 0x18
    return (struct.unpack_from('<H', binary, optional_header)[0] == 0x20B
            and struct.unpack_from('<H', binary, optional_header + 0x44)[0] == expected_subsystem)


class PeHeaderTests(unittest.TestCase):
    def test_gui_with_wrong_decoy_is_recognized(self):
        self.assertTrue(valid_pe32_plus(fake_pe(subsystem=2, decoy_subsystem=3), 2))

    def test_cli_with_wrong_decoy_is_recognized(self):
        self.assertTrue(valid_pe32_plus(fake_pe(subsystem=3, decoy_subsystem=2), 3))

    def test_decoy_never_defines_subsystem(self):
        self.assertFalse(valid_pe32_plus(fake_pe(subsystem=3, decoy_subsystem=2), 2))
        self.assertFalse(valid_pe32_plus(fake_pe(subsystem=2, decoy_subsystem=3), 3))

    def test_malformed_headers_rejected(self):
        cases = [
            fake_pe(machine=0x14C),
            fake_pe(magic=0x10B),
            fake_pe(optional_size=0x44),
            fake_pe(optional_size=0x300),
            b'MZ',
            bytes(512),
        ]
        for binary in cases:
            with self.subTest(length=len(binary)):
                self.assertFalse(valid_pe32_plus(binary, 2))

    def test_truncated_signature_and_oversized_offset_rejected(self):
        binary = bytearray(fake_pe())
        binary[0x80:0x84] = b"BAD!"
        self.assertFalse(valid_pe32_plus(binary, 2))
        binary = bytearray(fake_pe())
        struct.pack_into('<i', binary, 0x3C, 10_000)
        self.assertFalse(valid_pe32_plus(binary, 2))
        binary = bytearray(fake_pe())
        struct.pack_into('<i', binary, 0x3C, -1)
        self.assertFalse(valid_pe32_plus(binary, 2))

    def test_power_shell_uses_correct_optional_header_and_is_shared(self):
        source = VALIDATOR.read_text(encoding='utf-8')
        self.assertIn('$optionalHeader = $offset + 0x18', source)
        self.assertIn('$file.Position = $optionalHeader + 0x44', source)
        self.assertNotIn('$file.Position = $offset + 0x44', source)
        self.assertIn('$optionalSize -lt 0x46', source)
        self.assertIn('($optionalHeader + $optionalSize) -gt $file.Length', source)
        for file in (INSTALLER, BUILDER):
            self.assertIn(". (Join-Path $PSScriptRoot 'windows-pe.ps1')", file.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
