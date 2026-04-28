#!/usr/bin/env bash
# 카테고리 표 형식 검증 — 외부 PR 의 가장 흔한 사고(`|` 개수 어긋남)를 막는다.
#
# 검증 대상:
#   - references/ko-ai-signals.md 안 모든 카테고리 표
#   - 헤더가 정확히 `| 나쁨 | 자연스러움 |` 인 표는 모든 row 가 4 개의 `|` (= 3 개 셀 — leading/trailing 포함 시 4)
#   - 그 외 다중 컬럼 표 (예: 부록 A 의 4 컬럼) 도 헤더와 데이터 row 컬럼 수 일치 확인
#
# 실패 시 line 번호 + 위반 내용 출력 후 exit 1.
#
# 사용법:
#   bash scripts/lint-patterns.sh
#
# CI 에서 호출되며 PR 전 로컬 검증도 동일한 스크립트로 수행.

set -euo pipefail

FILE="references/ko-ai-signals.md"

if [[ ! -f "$FILE" ]]; then
  echo "ERR: $FILE 파일이 없습니다."
  exit 1
fi

# AWK 로 표 단위 검증.
# 표 = 연속된 `|` 로 시작하는 라인 묶음. 헤더 직후 separator (---) 라인이 와야 함.
# 각 표는 한 단위로 검증한다 — 헤더 컬럼 수 vs 데이터 row 컬럼 수.

awk '
function pipe_count(line,    n, i) {
  n = 0
  for (i = 1; i <= length(line); i++) {
    if (substr(line, i, 1) == "|") n++
  }
  return n
}

function trim(s) {
  sub(/^[[:space:]]+/, "", s)
  sub(/[[:space:]]+$/, "", s)
  return s
}

BEGIN {
  in_table = 0
  table_start = 0
  header_pipes = 0
  errors = 0
}

{
  line = $0
  trimmed = trim(line)

  # 표 시작 후보: `|` 로 시작 + 종료
  is_table_row = (trimmed ~ /^\|.*\|$/)

  if (!in_table && is_table_row) {
    in_table = 1
    table_start = NR
    header_pipes = pipe_count(trimmed)
    next
  }

  if (in_table) {
    if (!is_table_row) {
      in_table = 0
      next
    }

    # separator row (--- 만 있는 줄) 는 컬럼 수만 보고 통과
    is_separator = (trimmed ~ /^\|[[:space:]\-:|]+\|$/)

    cur_pipes = pipe_count(trimmed)

    if (cur_pipes != header_pipes) {
      printf "FAIL %s:%d 컬럼 수 불일치 — 헤더(%d번 줄)는 %d 개의 `|`, 이 줄은 %d 개\n",
        FILENAME, NR, table_start, header_pipes, cur_pipes
      printf "       row: %s\n", line
      errors++
    }
  }
}

END {
  if (errors > 0) {
    printf "\n표 형식 검증 실패: %d 건. 위 줄들의 `|` 개수를 헤더와 맞춰주세요.\n", errors
    exit 1
  } else {
    print "✓ 표 형식 검증 통과 — references/ko-ai-signals.md 의 모든 표가 정상."
  }
}
' "$FILE"
