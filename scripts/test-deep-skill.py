#!/usr/bin/env python3
"""Validate the deep skill's invocation metadata and reusable evaluation inputs."""
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/korean-humanizer-deep'


class DeepSkillContractTests(unittest.TestCase):
    def test_portable_frontmatter(self):
        text = (SKILL / 'SKILL.md').read_text()
        match = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
        self.assertIsNotNone(match, 'SKILL.md needs YAML frontmatter')
        fields = yaml.safe_load(match.group(1))
        self.assertIsInstance(fields, dict)
        self.assertEqual(fields.get('name'), SKILL.name)
        self.assertIsInstance(fields.get('description'), str)
        self.assertTrue(0 < len(fields['description'].strip()) <= 1024)
        self.assertLessEqual(len(text.splitlines()), 500)

    def test_codex_invocation(self):
        metadata = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text())
        interface = metadata['interface']
        for field in ['display_name', 'short_description', 'default_prompt']:
            self.assertIsInstance(interface[field], str)
            self.assertTrue(interface[field].strip())
        self.assertIn('$' + SKILL.name, interface['default_prompt'])

    def test_evaluation_contract(self):
        cases = json.loads((ROOT / 'eval/deep/evals.json').read_text())
        self.assertEqual(cases['skill_name'], SKILL.name)
        self.assertTrue(cases['evals'])
        ids = [case['id'] for case in cases['evals']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({case['should_trigger'] for case in cases['evals']}, {True, False})
        for case in cases['evals']:
            with self.subTest(case=case['id']):
                self.assertRegex(case['id'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                self.assertIsInstance(case['should_trigger'], bool)
                self.assertIsInstance(case['prompt'], str)
                self.assertTrue(case['prompt'].strip())
                if case['should_trigger']:
                    self.assertTrue(case['assertions'])
                    for assertion in case['assertions']:
                        self.assertIsInstance(assertion, str)
                        self.assertTrue(assertion.strip())
                for name in case.get('files', []):
                    path = (ROOT / 'eval/deep' / name).resolve()
                    self.assertTrue(path.is_relative_to((ROOT / 'eval/deep/fixtures').resolve()))
                    self.assertTrue(path.is_file(), name)


if __name__ == '__main__':
    unittest.main()
