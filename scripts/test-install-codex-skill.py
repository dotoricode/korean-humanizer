#!/usr/bin/env python3
"""Check development links, duplicate retirement and recoverable backups in a fake home."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_single_install_and_backups(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {**os.environ, 'HOME': tmp, 'CODEX_HOME': str(home / 'account')}
            env.pop('CODEX_SKILLS_DIR', None)
            old = [home / '.agents/skills/korean-humanizer', home / 'account/skills/korean-humanizer', home / '.codex/skills/korean-humanizer']
            for i, path in enumerate(old):
                path.mkdir(parents=True)
                (path / 'SKILL.md').write_text(f'old copy {i}')
            subprocess.run(['bash', str(ROOT / 'scripts/install-codex-skill.sh')], env=env, check=True, capture_output=True)
            self.assertTrue(old[0].is_symlink())
            self.assertEqual(old[0].resolve(), ROOT)
            self.assertFalse(old[1].exists())
            self.assertFalse(old[2].exists())
            backups = home / '.local/share/korean-humanizer/backups'
            self.assertEqual(sorted(p.read_text() for p in backups.rglob('SKILL.md')), [f'old copy {i}' for i in range(3)])
            before = sorted(str(p) for p in backups.rglob('*'))
            subprocess.run(['bash', str(ROOT / 'scripts/install-codex-skill.sh')], env=env, check=True, capture_output=True)
            self.assertEqual(before, sorted(str(p) for p in backups.rglob('*')))
            subprocess.run(['bash', str(ROOT / 'scripts/install-codex-skill.sh'), 'korean-humanizer-deep'], env=env, check=True, capture_output=True)
            self.assertEqual((home / '.agents/skills/korean-humanizer-deep').resolve(), ROOT / 'skills/korean-humanizer-deep')

    def test_custom_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {**os.environ, 'HOME': tmp, 'CODEX_HOME': str(home / 'account'), 'CODEX_SKILLS_DIR': str(home / 'custom')}
            shared = home / '.agents/skills/korean-humanizer'
            shared.mkdir(parents=True)
            (shared / 'SKILL.md').write_text('shared copy')
            subprocess.run(['bash', str(ROOT / 'scripts/install-codex-skill.sh')], env=env, check=True, capture_output=True)
            self.assertEqual((home / 'custom/korean-humanizer').resolve(), ROOT)
            self.assertFalse((home / '.codex/skills/korean-humanizer').exists())
            self.assertFalse(shared.exists())


if __name__ == '__main__':
    unittest.main()
