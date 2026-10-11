#!/usr/bin/env python3
"""Stable source consistency self-tests."""
import unittest
from pathlib import Path
from check_stable_release import ROOT,VERSION,validate,version_from_workspace,local_lock_versions

class StableReleaseTests(unittest.TestCase):
    def test_source_release_contract(self):
        self.assertEqual(validate(),49)
    def test_root_version_parser(self):
        self.assertEqual(version_from_workspace('[workspace]\nfoo=1\n[workspace.package]\nversion = "0.6.0"\nedition = "2024"\n'),VERSION)
    def test_lockfile_ignores_registry_dependencies(self):
        lock='[[package]]\nname = "local"\nversion = "0.6.0"\n\n[[package]]\nname = "external"\nversion = "0.5.0"\nsource = "registry+https://example.org"\n'
        self.assertEqual(local_lock_versions(lock),{'local':'0.6.0'})
    def test_lockfile_versions_are_not_unexpectedly_stale(self):
        result=local_lock_versions((ROOT/'Cargo.lock').read_text(encoding='utf8'))
        self.assertTrue(result)
        self.assertTrue(all(v==VERSION for v in result.values()))
    def test_ime_helper_is_only_in_test_module(self):
        source=(ROOT/'crates/ui-egui/src/panels/graphics.rs').read_text(encoding='utf-8')
        self.assertEqual(source.count('fn has_ime_edit('),1)
        self.assertIn('fn has_ime_edit(',source.split('mod korean_ime_tests {',1)[1])

if __name__=='__main__':unittest.main(verbosity=2)
