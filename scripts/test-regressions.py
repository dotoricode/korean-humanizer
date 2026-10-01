#!/usr/bin/env python3
"""Regression checks for fixture validation and isolated Codex installation (stdlib only)."""

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("eval_harness", REPO / "scripts/eval-harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="humanizer-test-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def fixture(self, raw, humanized, extra=""):
        path = self.root / "case.md"
        path.write_text(
            f"---\ndomain: blog\n{extra}\n---\n\n## Raw\n\n{raw}\n\n## Humanized\n\n{humanized}\n",
            encoding="utf-8",
        )
        return path

    def brand(self, preserve):
        path = self.root / "brand.md"
        path.write_text(f"---\npreserve: {preserve}\n---\n", encoding="utf-8")
        return path

    def test_length_floor_is_a_failure(self):
        result = harness.evaluate(self.fixture("이러한 서비스는 매우 좋습니다.", "이 서비스는 매우 좋습니다."))
        self.assertIn("m3", result["unexpected_failures"])
        self.assertEqual(harness.m3_verdict(0.90), "pass")

    def test_short_text_allows_one_changed_sentence(self):
        result = harness.evaluate(self.fixture("혁신적인 기술을 활용한 제품입니다.", "새로운 기술을 사용한 제품입니다."))
        self.assertTrue(result["overall_pass"])
        result = harness.evaluate(self.fixture("혁신적인 제품입니다. 혁신적인 제품입니다.", "새롭게 나온 제품입니다. 새롭게 나온 제품입니다."))
        self.assertIn("m1", result["unexpected_failures"])

    def test_sentence_budget_boundaries(self):
        raw = [
            "혁신적인 기술을 활용한 제품입니다.",
            "포괄적인 분석을 수행하는 서비스입니다.",
            "오늘은 오후에 회의가 있습니다.",
            "다음 주에는 배송을 시작합니다.",
            "문의는 담당자에게 부탁드립니다.",
            "서울 사무실은 오전에 문을 엽니다.",
            "부산 지점에서는 예약을 받습니다.",
            "대전에서 교육을 진행합니다.",
            "제주 센터로 자료를 보내주세요.",
            "광주 매장은 일요일에 쉽니다.",
        ]
        for count, edits, allowed in [(4, 1, True), (4, 2, False), (5, 1, True),
                                      (9, 2, False), (10, 2, True)]:
            with self.subTest(count=count, edits=edits):
                humanized = raw[:count]
                humanized[0] = "새로운 기술을 사용한 제품입니다."
                if edits == 2:
                    humanized[1] = "전체 내용을 살펴보는 서비스입니다."
                result = harness.evaluate(self.fixture(" ".join(raw[:count]), " ".join(humanized)))
                self.assertEqual(result["m1"]["modified"], edits)
                self.assertEqual(result["m1"]["pass"], allowed)

    def test_custom_cap_exact_boundary(self):
        raw = [chr(0xac00 + i) * 10 + "입니다." for i in range(50)]
        humanized = [chr(0xb000 + i) * 10 + "입니다." if i < 29 else sentence
                     for i, sentence in enumerate(raw)]
        result = harness.evaluate(self.fixture(
            " ".join(raw), " ".join(humanized), "cap: 58\nparagraph_cap: 100",
        ))
        self.assertEqual(result["m1"]["modified"], 29)
        self.assertTrue(result["overall_pass"])

    def test_preserve_only_requires_words_in_raw(self):
        profile = self.brand('["쉽게", "빠르게"]')
        result = harness.evaluate(self.fixture("쉽게 송금할 수 있어요.", "쉽게 송금할 수 있어요.", f"brand_voice: {profile}"))
        self.assertTrue(result["overall_pass"])
        self.assertEqual(result["m5"]["preserved"], ["쉽게"])

    def test_inline_and_block_preserve_detect_removal(self):
        for preserve in ['["딥다이브", "쉼표, 단어"]', '\n  - "딥다이브"\n  - "쉼표, 단어"']:
            with self.subTest(preserve=preserve):
                profile = self.brand(preserve)
                self.assertEqual(harness.parse_brand_voice_preserve(profile), ["딥다이브", "쉼표, 단어"])
                result = harness.evaluate(self.fixture("딥다이브를 해봅니다.", "자세하게 봅니다.", f"brand_voice: {profile}"))
                self.assertIn("m5", result["unexpected_failures"])

    def test_preserve_detects_lost_occurrences(self):
        profile = self.brand('["딥다이브"]')
        metric = harness.metric_brand_preserve("딥다이브 후 딥다이브", "딥다이브 후 자세한 검토", profile)
        self.assertEqual(metric["status"], "fail")

    def test_missing_required_trap_failure_is_rejected(self):
        trap = REPO / "eval/fixtures/youtube-02-trap-dache.md"
        self.assertTrue(harness.evaluate(trap)["overall_pass"])
        with patch.object(harness, "DACHE_PATTERN", __import__("re").compile(r"(?!)")):
            result = harness.evaluate(trap)
            self.assertFalse(result["overall_pass"])
            self.assertEqual(result["missing_required"], ["m4"])

    def test_known_risk_can_improve_without_being_a_trap(self):
        result = harness.evaluate(self.fixture("원문입니다.", "원문입니다.", "expected_failures: m4"))
        self.assertTrue(result["overall_pass"])
        self.assertEqual(result["missing_expected"], ["m4"])

    def test_empty_text_and_unknown_expectations_are_rejected(self):
        for raw, hum, extra in [("", "", ""), ("원문", "", ""), ("", "결과", ""), ("원문", "원문", "expected_failures: m99")]:
            with self.subTest(raw=raw, hum=hum, extra=extra):
                with self.assertRaises(ValueError):
                    harness.evaluate(self.fixture(raw, hum, extra))

    def test_cli_defaults_work_outside_repository(self):
        result = subprocess.run(["python3", str(REPO / "scripts/eval-harness.py"), "--strict", "--no-scorecard"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_wrapper_forwards_debug_and_output_flags(self):
        fixture = self.fixture("원문입니다.", "완전히 달라진 문장입니다.")
        for flags, code in [([], 1), (["--no-strict"], 0)]:
            result = subprocess.run(["bash", str(REPO / "scripts/eval-harness.sh"), *flags, "--fixtures-dir", str(fixture.parent), "--no-scorecard"], capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stderr + result.stdout)
            self.assertIn("0/1 fixtures pass", result.stdout)

    def test_wrapper_relative_paths_use_calling_directory(self):
        self.fixture("원문입니다.", "원문입니다.")
        result = subprocess.run(
            ["bash", str(REPO / "scripts/eval-harness.sh"), "--fixtures-dir", ".",
             "--scorecard", "report.md"], cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("1/1 fixtures pass", result.stdout)
        self.assertTrue((self.root / "report.md").is_file())

    def isolated_install(self, inside=False):
        skills = self.root / "active-skills"
        repo = skills / "korean-humanizer" if inside else self.root / "repo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy(REPO / "SKILL.md", repo / "SKILL.md")
        for name in ["install-codex-skill.sh", "check-codex-skill.sh"]:
            # Change only the home path in the scratch copy; never touch real user installs.
            source = (REPO / "scripts" / name).read_text().replace("$HOME", "$TASK_TEST_HOME")
            target = repo / "scripts" / name
            target.write_text(source)
            target.chmod(0o755)
        env = dict(os.environ, CODEX_SKILLS_DIR=str(skills), TASK_TEST_HOME=str(self.root / "user-home"))
        for _ in range(2):
            result = subprocess.run(["bash", str(repo / "scripts/install-codex-skill.sh")], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            check = subprocess.run(["bash", str(repo / "scripts/check-codex-skill.sh")], env=env, capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
        self.assertEqual((skills / "korean-humanizer").resolve(), repo.resolve())
        self.assertFalse(list(skills.glob("*.backup.*")))

    def test_install_and_reinstall_outside_skills_directory(self):
        self.isolated_install()

    def test_install_inside_skills_directory_keeps_repository(self):
        self.isolated_install(inside=True)


if __name__ == "__main__":
    unittest.main()
