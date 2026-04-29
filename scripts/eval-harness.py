#!/usr/bin/env python3
"""Eval harness — measures 4 heuristic metrics over eval/fixtures/*.md.

Metrics:
  M1: modified-sentence ratio  (cap, default 0.20)
  M2: per-paragraph modified-sentence cap  (paragraph_cap, default 3)
  M3: char-length ratio  (humanized / raw)
  M4: 다체 intrusion in speech domains

stdlib only (Python 3.8+).
"""

import argparse
import re
import sys
import os
from pathlib import Path
from datetime import datetime, timezone


SPEECH_DOMAINS = {"youtube", "podcast", "live", "lecture"}

# 다체 종결어미 (격식 / 글말체 typical endings)
# 종결 boundary: `.` `!` `?` `\n` 또는 문서 끝. Latin/숫자 뒤도 허용 (e.g. "AI다.").
DACHE_ENDINGS = (
    r"(?:다|한다|된다|있다|없다|였다|었다|겠다|이다|아니다|간다|온다|"
    r"난다|진다|봤다|샀다|썼다|줬다|왔다|갔다|냈다|섰다)"
)
DACHE_PATTERN = re.compile(rf"[가-힣A-Za-z0-9]{DACHE_ENDINGS}(?=[.!?\n]|$)")

# Sentence terminator regex (한국어/영어 모두 커버, decimal 보호)
# Split on . ! ? followed by whitespace or end. Don't split when preceded by digit.
SENT_SPLIT = re.compile(r"(?<=[.!?])(?<!\d\.)\s+")


# ---- I/O ---------------------------------------------------------------------

def parse_fixture(path: Path):
    text = path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not fm_match:
        raise ValueError(f"{path.name}: missing frontmatter (--- ... ---)")
    fm_raw, body = fm_match.groups()
    fm = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()

    raw_match = re.search(r"^##\s+Raw\s*\n(.*?)(?=^##\s+Humanized\s*\n)", body, re.DOTALL | re.MULTILINE)
    hum_match = re.search(r"^##\s+Humanized\s*\n(.*?)(?=^##\s+|\Z)", body, re.DOTALL | re.MULTILINE)
    if not raw_match or not hum_match:
        raise ValueError(f"{path.name}: missing '## Raw' or '## Humanized' section")
    return fm, raw_match.group(1).strip(), hum_match.group(1).strip()


# ---- Sentence split ----------------------------------------------------------

def split_paragraphs(text: str):
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def split_sentences_in_paragraph(para: str):
    para = para.replace("\n", " ").strip()
    if not para:
        return []
    parts = SENT_SPLIT.split(para)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        out.append(p)
    return out


def split_sentences_with_paragraph(text: str):
    """Returns list of (paragraph_idx, sentence_text)."""
    out = []
    for p_idx, para in enumerate(split_paragraphs(text)):
        for s in split_sentences_in_paragraph(para):
            out.append((p_idx, s))
    return out


# ---- Edit distance -----------------------------------------------------------

def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            ins = prev[j] + 1
            dele = curr[j - 1] + 1
            sub = prev[j - 1] + (0 if ca == cb else 1)
            curr.append(min(ins, dele, sub))
        prev = curr
    return prev[-1]


def normalized_edit_distance(a: str, b: str) -> float:
    if not a and not b:
        return 0.0
    return levenshtein(a, b) / max(len(a), len(b))


# ---- Metrics -----------------------------------------------------------------

def best_match_distances(raw_sents, hum_texts):
    """For each raw sentence, return its min normalized edit distance to any humanized sentence."""
    if not hum_texts:
        return [1.0] * len(raw_sents)
    out = []
    for _, r in raw_sents:
        out.append(min(normalized_edit_distance(r, h) for h in hum_texts))
    return out


# Threshold calibrated against long-form.md reference (52문장 / 9곳 modified
# = 17.3% per author). Empirically threshold=0.20 yields 8/45 = 17.8% — close
# match. Higher threshold = more lenient = more "small tweaks pass as kept".
SENTENCE_MOD_THRESHOLD = 0.20


def metric_modified_ratio(raw_sents, dists, threshold=SENTENCE_MOD_THRESHOLD):
    if not raw_sents:
        return {"ratio": 0.0, "modified": 0, "total": 0}
    modified = sum(1 for d in dists if d > threshold)
    return {
        "ratio": modified / len(raw_sents),
        "modified": modified,
        "total": len(raw_sents),
    }


def metric_paragraph_cap(raw_sents, dists, threshold=SENTENCE_MOD_THRESHOLD):
    by_para = {}
    for (p_idx, _), d in zip(raw_sents, dists):
        by_para.setdefault(p_idx, 0)
        if d > threshold:
            by_para[p_idx] += 1
    if not by_para:
        return {"max": 0, "by_para": {}}
    return {"max": max(by_para.values()), "by_para": by_para}


def metric_length_ratio(raw_text: str, hum_text: str):
    raw_len = len(raw_text)
    hum_len = len(hum_text)
    ratio = (hum_len / raw_len) if raw_len else 1.0
    return {"ratio": ratio, "raw_chars": raw_len, "hum_chars": hum_len}


def metric_dache_intrusion(raw_text: str, hum_text: str, domain: str):
    if domain not in SPEECH_DOMAINS:
        return {"status": "n/a", "raw_dache": 0, "hum_dache": 0}
    raw_count = len(DACHE_PATTERN.findall(raw_text))
    hum_count = len(DACHE_PATTERN.findall(hum_text))
    if raw_count == 0 and hum_count > 0:
        status = "fail"
    elif hum_count > raw_count + 1:
        # tolerate 1 extra (could be edge case in long texts)
        status = "warn"
    else:
        status = "pass"
    return {"status": status, "raw_dache": raw_count, "hum_dache": hum_count}


# ---- Verdict -----------------------------------------------------------------

def m3_verdict(ratio: float):
    if 0.5 <= ratio <= 1.05:
        return "pass"
    if (1.05 < ratio <= 1.20) or (0.30 <= ratio < 0.5):
        return "warn"
    return "fail"


def evaluate(fixture_path: Path):
    fm, raw, hum = parse_fixture(fixture_path)
    domain = fm.get("domain", "unknown").strip()
    cap = float(fm.get("cap", "20")) / 100.0
    para_cap = int(fm.get("paragraph_cap", 3))
    expected_failures = {
        x.strip().lower() for x in fm.get("expected_failures", "").split(",") if x.strip()
    }

    raw_sents = split_sentences_with_paragraph(raw)
    hum_sents = split_sentences_with_paragraph(hum)

    # Compute distances once, share across M1 and M2.
    hum_texts = [s for _, s in hum_sents]
    dists = best_match_distances(raw_sents, hum_texts)

    m1 = metric_modified_ratio(raw_sents, dists)
    m2 = metric_paragraph_cap(raw_sents, dists)
    m3 = metric_length_ratio(raw, hum)
    m4 = metric_dache_intrusion(raw, hum, domain)

    m1["pass"] = m1["ratio"] <= cap
    m2["pass"] = m2["max"] <= para_cap
    m3["verdict"] = m3_verdict(m3["ratio"])
    m3["pass"] = m3["verdict"] in ("pass", "warn")
    m4["pass"] = m4["status"] in ("pass", "n/a")

    actual_fails = {k for k, v in {"m1": m1, "m2": m2, "m3": m3, "m4": m4}.items()
                    if (k == "m3" and v["verdict"] == "fail") or (k != "m3" and not v["pass"])}

    # Subset semantics: fixture passes only if every actual failure was anticipated
    # via `expected_failures`. A new (unexpected) metric failing surfaces as fail
    # even when expected ones also fail — preventing silent swallows.
    unexpected_fails = actual_fails - expected_failures
    missing_expected = expected_failures - actual_fails  # informational only
    overall_pass = not unexpected_fails

    return {
        "fixture": fixture_path.name,
        "domain": domain,
        "cap_pct": int(cap * 100),
        "paragraph_cap": para_cap,
        "expected_failures": sorted(expected_failures),
        "actual_failures": sorted(actual_fails),
        "unexpected_failures": sorted(unexpected_fails),
        "missing_expected": sorted(missing_expected),
        "m1": m1,
        "m2": m2,
        "m3": m3,
        "m4": m4,
        "overall_pass": overall_pass,
    }


# ---- Scorecard ---------------------------------------------------------------

def write_scorecard(path: Path, results):
    total = len(results)
    passed = sum(1 for r in results if r["overall_pass"])
    failed = total - passed

    rows = []
    for r in results:
        m1 = r["m1"]
        m2 = r["m2"]
        m3 = r["m3"]
        m4 = r["m4"]
        m1_cell = f"{'✓' if m1['pass'] else '✗'} {m1['ratio']*100:.1f}% ({m1['modified']}/{m1['total']})"
        m2_cell = f"{'✓' if m2['pass'] else '✗'} max={m2['max']}"
        m3_cell = f"{m3['verdict']} {m3['ratio']:.2f}"
        m4_cell = f"{m4['status']} ({m4['raw_dache']}→{m4['hum_dache']})"
        if r["overall_pass"]:
            if r["expected_failures"]:
                overall = f"✓ (expected: {','.join(r['expected_failures'])})"
            else:
                overall = "✓"
        else:
            overall = f"✗ unexpected: {','.join(r['unexpected_failures'])}"
        rows.append(f"| {r['fixture']} | {r['domain']} | {m1_cell} | {m2_cell} | {m3_cell} | {m4_cell} | {overall} |")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    body = f"""<!-- Auto-generated by scripts/eval-harness.py — do not edit by hand. -->

# Eval scorecard

> Generated: {timestamp}
> Source: `eval/fixtures/*.md` ({total} fixtures)

## Summary

- Total fixtures: **{total}**
- Pass: **{passed}** ({passed/total*100:.1f}%)
- Fail: **{failed}**

## Per-fixture results

| Fixture | Domain | M1 (mod ratio) | M2 (para cap) | M3 (length) | M4 (다체) | Overall |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Legend

- **M1**: modified sentence count / total raw sentences. ✓ = within `cap` (default 20%).
- **M2**: max modified sentences in any paragraph. ✓ = within `paragraph_cap` (default 3).
- **M3**: char-length ratio (humanized / raw). `pass` 0.5–1.05, `warn` 0.30–0.5 or 1.05–1.20, `fail` <0.30 or >1.20.
- **M4**: 다체 intrusion check. Active only for speech domains (youtube/podcast/live/lecture); else `n/a`.
- Overall ✗ marked `(expected: m4)` etc. for trap fixtures — not an actual regression.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


# ---- CLI ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Eval harness for korean-humanizer fixtures.")
    parser.add_argument("--fixtures-dir", default="eval/fixtures")
    parser.add_argument("--scorecard", default="eval/scorecard.md")
    parser.add_argument(
        "--strict", action="store_true",
        help="exit 1 if any fixture fails (CI default).",
    )
    parser.add_argument(
        "--no-scorecard", action="store_true",
        help="skip writing scorecard.md (debug runs).",
    )
    args = parser.parse_args()

    fixtures_dir = Path(args.fixtures_dir)
    if not fixtures_dir.is_dir():
        print(f"ERR: {fixtures_dir} not found", file=sys.stderr)
        sys.exit(1)

    fixtures = sorted(fixtures_dir.glob("*.md"))
    if not fixtures:
        print(f"ERR: no fixtures in {fixtures_dir}", file=sys.stderr)
        sys.exit(1)

    results = []
    parse_errors = 0
    for f in fixtures:
        try:
            results.append(evaluate(f))
        except Exception as e:
            print(f"ERR parsing {f.name}: {e}", file=sys.stderr)
            parse_errors += 1

    if not results:
        sys.exit(1)

    if not args.no_scorecard:
        write_scorecard(Path(args.scorecard), results)

    fails = [r for r in results if not r["overall_pass"]]
    print(f"eval-harness: {len(results) - len(fails)}/{len(results)} fixtures pass"
          + (f" (parse errors: {parse_errors})" if parse_errors else ""))
    for r in fails:
        print(f"  ✗ {r['fixture']:30s} unexpected={r['unexpected_failures']} "
              f"actual={r['actual_failures']} expected={r['expected_failures']}")
        m = r["m1"]; print(f"      M1 ratio={m['ratio']*100:.1f}% mod={m['modified']}/{m['total']} cap={r['cap_pct']}%")
        m = r["m2"]; print(f"      M2 max={m['max']} cap={r['paragraph_cap']} by_para={m['by_para']}")
        m = r["m3"]; print(f"      M3 ratio={m['ratio']:.3f} verdict={m['verdict']}")
        m = r["m4"]; print(f"      M4 status={m['status']} raw_다체={m['raw_dache']} hum_다체={m['hum_dache']}")

    if args.strict and (fails or parse_errors):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
