#!/usr/bin/env python3
"""Run identical requests in fresh Codex contexts against two skill snapshots.

Use the active Codex model/configuration for both variants. This records outputs
and structural checks; semantic preservation still requires reading the results.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
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


def check_format(response):
    changes = response.split("## 주요 변경 (최대 5개)")
    entries = list(re.finditer(r"^([ \t]*)([-+*]|\d+[.)])\s+", changes[1], re.M)) if len(changes) == 2 else []
    valid = (response.startswith("## Humanized\n") and len(changes) == 2
             and 0 < len(entries) <= 5
             and all(not e[1] and e[2] == "-" for e in entries)
             and response.rstrip().endswith(
                 "*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*"))
    return valid, len(entries)


def catalog_was_read(item, work):
    if item.get("exit_code") != 0 or not item.get("aggregated_output", "").strip():
        return False
    try:
        args = shlex.split(item["command"])
        if len(args) == 3 and Path(args[0]).name in ("sh", "bash", "zsh") and args[1] in ("-c", "-lc"):
            args = shlex.split(args[2])
    except (ValueError, KeyError):
        return False
    if args[:2] == ["cat", "--"]:
        args.pop(1)
    if len(args) != 2 or args[0] != "cat":
        return False
    catalog = work / "skill/references/ko-ai-signals.md"
    if (work / args[1]).resolve() != catalog.resolve():
        return False
    headings = catalog.read_text(encoding="utf-8").splitlines()
    return bool(headings) and headings[0] in item["aggregated_output"]


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
    failures = []
    try:
        result = subprocess.run(command, input=prompt, text=True, encoding="utf-8",
                                capture_output=True, timeout=600)
    except subprocess.TimeoutExpired as exc:
        # TimeoutExpired can carry bytes even with text=True.
        decode = lambda value: value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
        result = subprocess.CompletedProcess(command, 124, decode(exc.stdout), decode(exc.stderr))
        failures.append({"type": "timeout", "message": "Codex exceeded the 600-second timeout."})
    except OSError as exc:
        result = subprocess.CompletedProcess(command, 127, "", str(exc))
        failures.append({"type": "launch_error", "message": str(exc)})
    events = []
    for line in result.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    response = output.read_text(encoding="utf-8") if output.exists() else ""
    executions = [event["item"] for event in events
                  if event.get("type") == "item.completed"
                  and event.get("item", {}).get("type") == "command_execution"]
    command_results = [{"command": e["command"], "exit_code": e.get("exit_code"),
                        "aggregated_output": e.get("aggregated_output", "")}
                       for e in executions]
    valid, count = check_format(response)
    item = {"case_id": case["id"], "variant": variant,
            "prompt": prompt, "prompt_sha256": sha(prompt.encode()),
            "seconds": round(time.monotonic() - start, 2),
            "exit_code": result.returncode, "response": response,
            "format_checks_passed": valid,
            "change_entry_count": count,
            "catalog_read_observed": any(catalog_was_read(e, work) for e in command_results),
            "tool_commands": [e["command"] for e in command_results],
            "command_results": command_results,
            "usage": [e.get("usage") for e in events if e.get("type") == "turn.completed"],
            "errors": failures + [e for e in events if e.get("type") in ("error", "turn.failed")],
            "stdout": result.stdout if result.returncode else "",
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
        runs = []
        record = {"baseline_commit": args.baseline_commit,
            "codex_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
            "configured_profile": profile,
            "invocation": "Fresh codex exec context; active model/config, read-only sandbox; identical relative skill path and prompt per pair; no output postprocessing.",
            "source_manifests": manifests, "cases": cases, "runs": runs}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(run, *task): task for task in tasks}
            for future in as_completed(futures):
                case, variant, _, _ = futures[future]
                try:
                    runs.append(future.result())
                except Exception as exc:
                    runs.append({"case_id": case["id"], "variant": variant,
                                 "exit_code": 1, "response": "",
                                 "errors": [{"type": type(exc).__name__, "message": str(exc)}]})
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output.parent,
                                                 delete=False) as checkpoint:
                    json.dump(record, checkpoint, ensure_ascii=False, indent=2)
                    checkpoint.write("\n")
                Path(checkpoint.name).replace(args.output)
    if any(r["exit_code"] or not r["response"] for r in runs):
        raise SystemExit("One or more runs failed; inspect the recorded errors.")


if __name__ == "__main__":
    main()
