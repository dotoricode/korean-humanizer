#!/usr/bin/env python3
"""Run fresh Codex contexts on isolated fixtures; retain raw evidence."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads((ROOT / 'eval/deep/evals.json').read_text())['evals']


def snapshot(directory):
    return {
        str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob('*') if p.is_file()
    }


def run(output, case, variant, baseline_skill=None):
    destination = output / (case['id'] + '-' + variant)
    destination.mkdir()
    workspace = destination / 'workspace'
    fixture = ROOT / 'eval/deep/fixtures' / case['id']
    if fixture.is_dir():
        shutil.copytree(fixture, workspace)
    else:
        workspace.mkdir()
    # Keep candidate instructions portable and inside the run's sandbox.
    if variant == 'candidate' or baseline_skill:
        source = ROOT / 'skills/korean-humanizer-deep' if variant == 'candidate' else baseline_skill
        skill = destination / source.name
        shutil.copytree(source, skill)
        instruction = f'Read and apply the skill at {skill}/SKILL.md.\n'
    else:
        instruction = ''
    prompt = instruction + case['prompt']
    (destination / 'prompt.txt').write_text(prompt)
    before = snapshot(workspace)
    started = time.monotonic()
    command = [
        'codex', 'exec', '--ephemeral', '--skip-git-repo-check',
        '--ignore-user-config', '-C', str(workspace), '-s', 'workspace-write',
        '--json', '-o', str(destination / 'response.md'), prompt,
    ]
    with (destination / 'events.jsonl').open('w') as stdout, (destination / 'stderr.log').open('w') as stderr:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=600)
    after = snapshot(workspace)
    record = {
        'eval_id': case['id'], 'variant': variant, 'exit_code': result.returncode,
        'skill_sha256': hashlib.sha256((skill / 'SKILL.md').read_bytes()).hexdigest() if variant == 'candidate' or baseline_skill else None,
        'duration_ms': round((time.monotonic() - started) * 1000),
        'changed_files': sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k)),
        'before': before, 'after': after,
    }
    (destination / 'record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k not in ('before', 'after')}, ensure_ascii=False), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New directory for raw run evidence')
    parser.add_argument('--cases', nargs='+', help='Case IDs to run')
    parser.add_argument('--baseline-skill', type=Path, help='Prior skill snapshot; otherwise use no explicit skill')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    cases = [case for case in CASES if case['should_trigger'] and (not args.cases or case['id'] in args.cases)]
    if args.cases and set(args.cases) != {case['id'] for case in cases}:
        parser.error('--cases must name should-trigger cases')
    jobs = [(case, variant) for case in cases for variant in ('candidate', 'baseline')]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run, output, case, variant, args.baseline_skill) for case, variant in jobs]
        records = [future.result() for future in futures]
    (output / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    if any(record['exit_code'] for record in records):
        raise SystemExit('One or more runs failed; inspect stderr.log and events.jsonl before grading.')


if __name__ == '__main__':
    main()
