#!/usr/bin/env bash
# Eval harness wrapper — calls scripts/eval-harness.py with strict mode.
#
# 4 metric (수정 비율 / 단락 cap / 길이 비율 / 다체 보존) 을 eval/fixtures/*.md
# 에 적용하고 eval/scorecard.md 를 갱신한다. 실패 fixture 가 1 개라도 있으면 exit 1.
#
# 사용법:
#   bash scripts/eval-harness.sh           # CI / 머지 검증용 (strict)
#   bash scripts/eval-harness.sh --no-strict   # 로컬 디버깅

set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "ERR: $PYTHON not found. Install Python 3.8+ or set PYTHON=..." >&2
  exit 127
fi

# Default: strict. Allow override via flag.
ARGS=("--strict")
if [[ "${1:-}" == "--no-strict" ]]; then
  ARGS=()
fi

exec "$PYTHON" scripts/eval-harness.py "${ARGS[@]}"
