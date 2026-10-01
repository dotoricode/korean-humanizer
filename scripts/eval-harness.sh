#!/usr/bin/env bash
# Eval harness wrapper — calls scripts/eval-harness.py with strict mode.
#
# M1-M5 (수정 비율 / 단락 cap / 길이 비율 / 다체 / brand 보존)를 eval/fixtures/*.md
# 에 적용하고 eval/scorecard.md를 갱신한다. 예상 밖 실패나 필수 trap 탐지 누락 시 exit 1.
#
# 사용법:
#   bash scripts/eval-harness.sh           # CI / 머지 검증용 (strict)
#   bash scripts/eval-harness.sh --no-strict   # 로컬 디버깅

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "ERR: $PYTHON not found. Install Python 3.8+ or set PYTHON=..." >&2
  exit 127
fi

# CLI options (including --no-strict) override the strict default.
exec "$PYTHON" "$SCRIPT_DIR/eval-harness.py" --strict "$@"
