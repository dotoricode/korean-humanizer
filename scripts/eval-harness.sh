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

PROBE='import sys; print("GJC_PYTHON_OK|%d.%d.%d" % sys.version_info[:3]); raise SystemExit(0 if sys.version_info >= (3, 8) else 1)'

try_candidate() {
  local stdout_file stderr_file status stdout stdout_lines version major minor valid_sentinel=false

  stdout_file=$(mktemp)
  stderr_file=$(mktemp)
  if "$@" -c "$PROBE" >"$stdout_file" 2>"$stderr_file"; then
    status=0
  else
    status=$?
  fi

  stdout=$(<"$stdout_file")
  stdout_lines=$(wc -l <"$stdout_file")
  rm -f "$stdout_file"

  if [[ "$stdout_lines" -eq 1 ]] && [[ "$stdout" =~ ^GJC_PYTHON_OK\|([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
    valid_sentinel=true
    major=${BASH_REMATCH[1]}
    minor=${BASH_REMATCH[2]}
    version="$major.$minor.${BASH_REMATCH[3]}"
  fi

  if [[ "$valid_sentinel" == true ]] && (( major < 3 || (major == 3 && minor < 8) )); then
    TRY_REASON="Python $version is below 3.8"
  elif (( status != 0 )); then
    TRY_REASON="probe exit=$status"
  elif [[ "$valid_sentinel" != true ]]; then
    TRY_REASON="missing or invalid Python sentinel"
  elif [[ -s "$stderr_file" ]]; then
    TRY_REASON="probe wrote stderr"
  else
    TRY_VERSION="$version"
    rm -f "$stderr_file"
    return 0
  fi

  rm -f "$stderr_file"
  return 1
}

display_candidate() {
  local display=""
  local part
  for part in "$@"; do
    if [[ -n "$display" ]]; then
      display+=" "
    fi
    display+="$part"
  done
  printf '%s' "$display"
}

select_candidate() {
  local display

  if [[ -n "${PYTHON:-}" ]]; then
    if [[ "$PYTHON" == "py -3" ]]; then
      if try_candidate py -3; then
        selected=(py -3)
      else
        printf 'eval-harness: PYTHON override candidate=py -3 rejected: %s; set PYTHON to an executable pathname or unset it\n' "$TRY_REASON" >&2
        exit 1
      fi
    elif try_candidate "$PYTHON"; then
      selected=("$PYTHON")
    else
      printf 'eval-harness: PYTHON override candidate=%s rejected: %s; set PYTHON to an executable pathname or unset it\n' "$PYTHON" "$TRY_REASON" >&2
      exit 1
    fi
  else
    local -a candidate
    for candidate in python3 python "py -3"; do
      if [[ "$candidate" == "py -3" ]]; then
        candidate=(py -3)
      else
        candidate=("$candidate")
      fi
      display=$(display_candidate "${candidate[@]}")
      if try_candidate "${candidate[@]}"; then
        selected=("${candidate[@]}")
        break
      fi
      printf 'eval-harness: candidate=%s rejected: %s\n' "$display" "$TRY_REASON" >&2
    done
    if [[ ${#selected[@]} -eq 0 ]]; then
      exit 1
    fi
  fi

  printf 'eval-harness: selected candidate=%s version=%s\n' "$(display_candidate "${selected[@]}")" "$TRY_VERSION" >&2
}

# Default: strict. Allow override via flag.
ARGS=("--strict")
if [[ "${1:-}" == "--no-strict" ]]; then
  ARGS=()
fi

selected=()
TRY_REASON=""
TRY_VERSION=""
select_candidate

exec "${selected[@]}" scripts/eval-harness.py "${ARGS[@]}"
