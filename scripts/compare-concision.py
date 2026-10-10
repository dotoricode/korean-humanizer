#!/usr/bin/env python3
"""Run identical requests in fresh Codex contexts against two skill snapshots.

Use the active Codex model/configuration for both variants. This records outputs
and structural checks; semantic preservation still requires reading the results.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(source, target):
    target.mkdir(parents=True)
    for name in ("SKILL.md", "PROMPT.md", "PROMPT.short.md", "LICENSE"):
        shutil.copy2(source / name, target / name)
    for name in ("references", "examples"):
        shutil.copytree(source / name, target / name)
    return {str(p.relative_to(target)): sha(p.read_bytes())
            for p in sorted(target.rglob("*")) if p.is_file()}


def run(case, variant, source, root):
    work = root / (case["id"] + "-" + variant)
    work.mkdir()
    snapshot(source, work / "skill")
    prompt = ("이 작업에는 ./skill/SKILL.md와 그 안에서 지정한 참조만 사용하세요. "
              "다른 설치본은 사용하지 마세요.\n\n"
              + case["request"] + "\n\n" + case["input"])
    # One shared prompt construction ensures byte-identical requests per pair.
    output = work / "response.md"
    command = ["codex", "exec", "--ephemeral", "--json", "--color", "never",
               "--sandbox", "read-only", "--skip-git-repo-check",
               "--cd", str(work), "--output-last-message", str(output), "-"]
    start = time.monotonic()
    result = subprocess.run(command, input=prompt, text=True, encoding="utf-8",
                            capture_output=True, timeout=600)
    events = []
    for line in result.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    response = output.read_text(encoding="utf-8") if output.exists() else ""
    commands = [event["item"]["command"] for event in events
                if event.get("type") == "item.completed"
                and event.get("item", {}).get("type") == "command_execution"]
    changes = response.split("## 주요 변경 (최대 5개)", 1)
    count = len(re.findall(r"^- ", changes[1], flags=re.M)) if len(changes) == 2 else 0
    item = {"case_id": case["id"], "variant": variant,
            "prompt": prompt, "prompt_sha256": sha(prompt.encode()),
            "seconds": round(time.monotonic() - start, 2),
            "exit_code": result.returncode, "response": response,
            "format_checks_passed": response.startswith("## Humanized\n")
                and len(changes) == 2 and count <= 5
                and "*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*" in response,
            "change_entry_count": count,
            "catalog_read_observed": any("ko-ai-signals.md" in c for c in commands),
            "tool_commands": commands,
            "usage": [e.get("usage") for e in events if e.get("type") == "turn.completed"],
            "errors": [e for e in events if e.get("type") in ("error", "turn.failed")],
            "stderr": result.stderr if result.returncode else ""}
    print(f'{variant} {case["id"]}: exit={result.returncode}, '
          f'format={item["format_checks_passed"]}, {item["seconds"]}s', flush=True)
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=2, choices=(1, 2))
    args = parser.parse_args()
    config_path = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    config = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    profile = {key: match.group(1) for key in ("model", "model_reasoning_effort")
               if (match := re.search(r'^' + key + r'\s*=\s*"([^"]+)"', config, re.M))}
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
    assert cases and len({case["id"] for case in cases}) == len(cases)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kh-concision-") as temp:
        root = Path(temp)
        sources = {v: root / v / "korean-humanizer" for v in ("baseline", "candidate")}
        manifests = {v: snapshot(src.resolve(), sources[v]) for v, src in
                     (("baseline", args.baseline), ("candidate", args.candidate))}
        tasks = [(c, v, sources[v], root) for c in cases for v in sources]
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            runs = list(pool.map(lambda task: run(*task), tasks))
    record = {"baseline_commit": args.baseline_commit,
        "codex_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "configured_profile": profile,
        "invocation": "Fresh codex exec context; active model/config, read-only sandbox; identical relative skill path and prompt per pair; no output postprocessing.",
        "source_manifests": manifests, "cases": cases, "runs": runs}
    for case in cases:
        pair = [r for r in runs if r["case_id"] == case["id"]]
        assert len(pair) == 2 and pair[0]["prompt"] == pair[1]["prompt"]
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if any(r["exit_code"] or not r["response"] for r in runs):
        raise SystemExit("One or more runs failed; inspect the recorded errors.")


if __name__ == "__main__":
    main()
