#!/usr/bin/env python3
"""Regression checks for comparison evidence; never calls a model."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("comparison", Path(__file__).with_name("compare-concision.py"))
comparison = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparison)
GUIDANCE = "*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*"


def response(entries):
    return "## Humanized\n\n본문입니다.\n\n## 주요 변경 (최대 5개)\n" + entries + "\n\n" + GUIDANCE


class ComparisonTests(unittest.TestCase):
    def test_change_limit_and_supported_list_forms(self):
        for marker in ("-", "*", "+", "1.", "1)", "  -"):
            with self.subTest(marker=marker):
                valid, count = comparison.check_format(response("\n".join(f"{marker} 수정" for _ in range(6))))
                self.assertFalse(valid)
                self.assertEqual(count, 6)
        for entries in ("* 수정", "1. 수정", "- 수정\n  - 추가 설명", "수정 여섯 개", ""):
            self.assertFalse(comparison.check_format(response(entries))[0])
        self.assertEqual(comparison.check_format(response("\n".join("- 수정" for _ in range(5)))), (True, 5))

    def test_catalog_requires_successful_read_not_filename_mention(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            catalog = work / "skill/references/ko-ai-signals.md"
            catalog.parent.mkdir(parents=True)
            catalog.write_text("# Catalog\nRules", encoding="utf-8")
            for command in ("cat ./skill/references/ko-ai-signals.md",
                            "/bin/zsh -lc 'cat ./skill/references/ko-ai-signals.md'",
                            f"cat -- {catalog}"):
                item = {"command": command, "exit_code": 0, "aggregated_output": "# Catalog\nRules"}
                self.assertTrue(comparison.catalog_was_read(item, work))
            for command, code, output in (
                ("cat ./skill/references/ko-ai-signals.md", 1, "No such file"),
                ("cat ./skill/references/ko-ai-signals.md", None, "# Catalog"),
                ("cat ./skill/references/ko-ai-signals.md", 0, ""),
                ("ls ./skill/references/ko-ai-signals.md", 0, "# Catalog"),
                ("echo ./skill/references/ko-ai-signals.md", 0, "# Catalog"),
                ("cat ./other/ko-ai-signals.md", 0, "# Catalog"),
                ("cat ./skill/references/ko-ai-signals.md > /dev/null", 0, "# Catalog"),
            ):
                with self.subTest(command=command, code=code):
                    self.assertFalse(comparison.catalog_was_read(
                        {"command": command, "exit_code": code, "aggregated_output": output}, work))

    def test_timeout_keeps_completed_and_partial_responses(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            for name in ("SKILL.md", "PROMPT.md", "PROMPT.short.md", "LICENSE"):
                (source / name).write_text("fixture", encoding="utf-8")
            (source / "examples").mkdir()
            (source / "references").mkdir()
            (source / "references/ko-ai-signals.md").write_text("# Catalog\nRules", encoding="utf-8")
            cases = root / "cases.json"
            cases.write_text(json.dumps({"cases": [{"id": "case", "request": "다듬어줘", "input": "본문"}]}), encoding="utf-8")
            output = root / "result.json"
            successful = response("- 수정")
            event = {"type": "item.completed", "item": {"type": "command_execution",
                     "command": "cat ./skill/references/ko-ai-signals.md", "exit_code": 0,
                     "aggregated_output": "# Catalog\nRules"}}
            stdout = json.dumps(event) + "\n"

            def fake_run(command, **kwargs):
                response_path = Path(command[command.index("--output-last-message") + 1])
                if "candidate" in str(response_path):
                    response_path.write_text("partial response", encoding="utf-8")
                    raise subprocess.TimeoutExpired(command, 600, output=stdout.encode(), stderr=b"timeout")
                response_path.write_text(successful, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout, "")

            argv = ["compare", "--baseline", str(source), "--baseline-commit", "fixture",
                    "--candidate", str(source), "--cases", str(cases), "--output", str(output), "--jobs", "1"]
            with patch.object(sys, "argv", argv), patch.object(comparison.subprocess, "run", side_effect=fake_run), \
                    patch.object(comparison.subprocess, "check_output", return_value="codex fixture"):
                with self.assertRaises(SystemExit):
                    comparison.main()
            record = json.loads(output.read_text(encoding="utf-8"))
            runs = {r["variant"]: r for r in record["runs"]}
            self.assertEqual(runs["baseline"]["response"], successful)
            self.assertEqual(runs["baseline"]["exit_code"], 0)
            self.assertTrue(runs["baseline"]["catalog_read_observed"])
            self.assertEqual(runs["candidate"]["exit_code"], 124)
            self.assertEqual(runs["candidate"]["response"], "partial response")
            self.assertEqual(runs["candidate"]["errors"][0]["type"], "timeout")
            self.assertEqual(runs["candidate"]["stderr"], "timeout")
            self.assertEqual(runs["candidate"]["command_results"][0]["exit_code"], 0)
            self.assertEqual(runs["baseline"]["prompt"], runs["candidate"]["prompt"])

    def test_recorded_responses_still_pass_stricter_format_check(self):
        path = Path(__file__).resolve().parent.parent / "eval/model-runs/six-rules-2026-10-10.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(record["runs"]), 16)
        for run in record["runs"]:
            with self.subTest(case=run["case_id"], variant=run["variant"]):
                self.assertEqual(comparison.check_format(run["response"]), (True, run["change_entry_count"]))


if __name__ == "__main__":
    unittest.main()
