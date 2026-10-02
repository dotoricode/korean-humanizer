#!/usr/bin/env python3
"""Check ZIP provenance and rejection of uncommitted package sources."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('packager', REPO / 'scripts/package-skill.py')
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackageTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix='kh-package-test-')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name) / 'repo'
        self.root.mkdir()
        self.output = Path(scratch.name) / 'output'
        self.git('init', '-q')
        for key, field in [('user.name', '%an'), ('user.email', '%ae')]:
            value = subprocess.check_output(['git', 'log', '-1', f'--format={field}'],
                                            cwd=REPO, text=True).strip()
            self.git('config', key, value)
        (self.root / 'docs/distribution').mkdir(parents=True)
        (self.root / 'SKILL.md').write_text('Skill instructions\n')
        (self.root / 'LICENSE').write_text('MIT\n')
        (self.root / 'docs/evidence.md').write_text('Committed evidence\n')
        (self.root / 'docs/distribution/PACKAGE-README.md').write_text('[Evidence](docs/evidence.md)\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'Package provenance fixture')
        root_patch = patch.object(packager, 'ROOT', self.root)
        files_patch = patch.object(packager, 'FILES', ['SKILL.md', 'LICENSE'])
        root_patch.start()
        files_patch.start()
        self.addCleanup(root_patch.stop)
        self.addCleanup(files_patch.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True).strip()

    def test_clean_source_has_exact_commit_and_reproducible_archive(self):
        packager.build(self.output)
        manifest = json.loads((self.output / 'manifest.json').read_text())
        commit = self.git('rev-parse', 'HEAD')
        self.assertEqual(manifest['source_commit'], commit)
        self.assertIn('docs/distribution/PACKAGE-README.md', manifest['source_file_sha256'])
        archive = next(self.output.glob('*.zip'))
        with ZipFile(archive) as zf:
            self.assertEqual(zf.read('README.md').decode(),
                             f'[Evidence](https://github.com/dotoricode/korean-humanizer/blob/{commit}/docs/evidence.md)\n')
        first = archive.read_bytes()
        packager.build(self.output)
        self.assertEqual(first, archive.read_bytes())
        self.assertEqual(manifest['archive_sha256'], hashlib.sha256(first).hexdigest())

    def test_modified_package_instructions_are_rejected(self):
        (self.root / 'docs/distribution/PACKAGE-README.md').write_text('Uncommitted instructions\n')
        with self.assertRaisesRegex(ValueError, 'clean'):
            packager.build(self.output)
        self.assertFalse(self.output.exists())

    def test_untracked_source_is_rejected(self):
        (self.root / 'extra.md').write_text('Untracked source\n')
        with self.assertRaisesRegex(ValueError, 'clean'):
            packager.build(self.output)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
