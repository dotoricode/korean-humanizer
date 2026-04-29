#!/usr/bin/env bash
# 카테고리 표 형식 검증 — 외부 PR 의 가장 흔한 사고(`|` 개수 어긋남)를 막는다.
#
# 검증 대상:
#   - references/ko-ai-signals.md 안 모든 카테고리 표
#   - 헤더 컬럼 수 vs 데이터 row 컬럼 수 일치
#   - 표준 패턴 표 (헤더에 "나쁨" + "자연스러움" 포함) 는 반드시 "빈도" 컬럼도 포함
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
  header_line = ""
  needs_freq = 0
  errors = 0
}

{
  line = $0
  trimmed = trim(line)

  is_table_row = (trimmed ~ /^\|.*\|$/)

  if (!in_table && is_table_row) {
    in_table = 1
    table_start = NR
    header_pipes = pipe_count(trimmed)
    header_line = trimmed
    # 표준 패턴 표 식별: 헤더에 "나쁨" 과 "자연스러움" 동시 포함
    needs_freq = (index(header_line, "나쁨") > 0 && index(header_line, "자연스러움") > 0)
    if (needs_freq && index(header_line, "빈도") == 0) {
      printf "FAIL %s:%d 표준 패턴 표 헤더에 \"빈도\" 컬럼이 빠졌습니다.\n", FILENAME, NR
      printf "       header: %s\n", line
      printf "       expected: | 나쁨 | 자연스러움 | 빈도 |\n"
      errors++
    }
    next
  }

  if (in_table) {
    if (!is_table_row) {
      in_table = 0
      next
    }

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
    printf "\n표 형식 검증 실패: %d 건. 위 줄들을 확인해주세요.\n", errors
    exit 1
  } else {
    print "✓ 표 형식 검증 통과 — references/ko-ai-signals.md 의 모든 표가 정상."
  }
}
' "$FILE"
