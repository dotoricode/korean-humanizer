#!/usr/bin/env bash
# 카테고리 표 형식 검증 — 외부 PR 의 가장 흔한 사고(`|` 개수 어긋남)를 막는다.
#
# 검증 대상:
#   - references/ko-ai-signals.md 안 모든 카테고리 표
#   - 헤더 컬럼 수 vs 데이터 row 컬럼 수 일치
#   - 표준 패턴 표 (헤더에 "나쁨" + "자연스러움" 포함) 는 반드시
#     "빈도" 컬럼 + "적용 도메인" 컬럼 모두 포함 (v0.8 카탈로그 v2)
#   - "적용 도메인" 컬럼 값은 부록 F 의 valid 도메인 코드여야 함
#     (all / informal / formal / 12 도메인 콤마 리스트, 혼용 가능)
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

function valid_domain_token(tok,    i) {
  # tok 이 단일 도메인 코드 또는 shorthand 인지
  for (i in valid_domains) {
    if (i == tok) return 1
  }
  return 0
}

# 셀 값에서 도메인 컬럼 valid 검증.
# valid: "all" 단독, 또는 콤마-구분 known 코드 리스트 (공백 허용).
# invalid: "all" 과 다른 코드 혼용, unknown 코드.
function validate_domain_cell(cell, line_no, raw_line,    n, parts, i, tok, has_all, has_other, errs) {
  cell = trim(cell)
  if (cell == "") {
    printf "FAIL %s:%d 적용 도메인 컬럼이 비어 있습니다.\n", FILENAME, line_no
    printf "       row: %s\n", raw_line
    errors++
    return
  }

  n = split(cell, parts, /[[:space:]]*,[[:space:]]*/)
  has_all = 0
  has_other = 0
  for (i = 1; i <= n; i++) {
    tok = trim(parts[i])
    if (tok == "") continue
    if (!valid_domain_token(tok)) {
      printf "FAIL %s:%d 적용 도메인 코드가 잘못됨: \"%s\"\n", FILENAME, line_no, tok
      printf "       row: %s\n", raw_line
      printf "       valid: all / informal / formal / blog / marketing / email / linkedin / youtube / newsletter / wiki / academic / news / chat / review / b2b-message\n"
      errors++
      return
    }
    if (tok == "all") has_all = 1
    else has_other = 1
  }
  if (has_all && has_other) {
    printf "FAIL %s:%d \"all\" 은 단독 사용만 가능 (다른 코드와 혼용 금지).\n", FILENAME, line_no
    printf "       row: %s\n", raw_line
    errors++
  }
}

BEGIN {
  in_table = 0
  table_start = 0
  header_pipes = 0
  header_line = ""
  needs_freq = 0
  needs_domain = 0
  domain_col_idx = 0   # "적용 도메인" 컬럼의 인덱스 (1-based, | split 기준 데이터 컬럼)
  errors = 0

  # 부록 F 의 valid 도메인 코드 + shorthand
  valid_domains["all"] = 1
  valid_domains["informal"] = 1
  valid_domains["formal"] = 1
  valid_domains["blog"] = 1
  valid_domains["marketing"] = 1
  valid_domains["email"] = 1
  valid_domains["linkedin"] = 1
  valid_domains["youtube"] = 1
  valid_domains["newsletter"] = 1
  valid_domains["wiki"] = 1
  valid_domains["academic"] = 1
  valid_domains["news"] = 1
  valid_domains["chat"] = 1
  valid_domains["review"] = 1
  valid_domains["b2b-message"] = 1
}

{
  line = $0
  trimmed = trim(line)

  is_table_row = (trimmed ~ /^\|.*\|$/)
  # 마크다운 정렬 행 (| --- | --- |) 은 헤더 다음 줄. 데이터로 취급하지 않음.
  is_align_row = (trimmed ~ /^\|[[:space:]]*[-:]+[[:space:]]*(\|[[:space:]]*[-:]+[[:space:]]*)+\|$/)

  if (!in_table && is_table_row) {
    in_table = 1
    table_start = NR
    header_pipes = pipe_count(trimmed)
    header_line = trimmed

    # 표준 패턴 표 식별: 헤더에 "나쁨" 과 "자연스러움" 동시 포함
    needs_freq = (index(header_line, "나쁨") > 0 && index(header_line, "자연스러움") > 0)
    needs_domain = needs_freq
    domain_col_idx = 0

    if (needs_freq && index(header_line, "빈도") == 0) {
      printf "FAIL %s:%d 표준 패턴 표 헤더에 \"빈도\" 컬럼이 빠졌습니다.\n", FILENAME, NR
      printf "       header: %s\n", line
      printf "       expected: | 나쁨 | 자연스러움 | 빈도 | 적용 도메인 |\n"
      errors++
    }
    if (needs_domain && index(header_line, "적용 도메인") == 0) {
      printf "FAIL %s:%d 표준 패턴 표 헤더에 \"적용 도메인\" 컬럼이 빠졌습니다 (v0.8 카탈로그 v2).\n", FILENAME, NR
      printf "       header: %s\n", line
      printf "       expected: | 나쁨 | 자연스러움 | 빈도 | 적용 도메인 |\n"
      errors++
    }

    # "적용 도메인" 컬럼 인덱스 찾기 (헤더 split 기준)
    if (needs_domain) {
      n_cols = split(header_line, hcols, /\|/)
      # split 결과: hcols[1] = "" (앞 |), hcols[2..n-1] = 셀, hcols[n] = "" (뒤 |)
      for (k = 2; k < n_cols; k++) {
        if (index(trim(hcols[k]), "적용 도메인") > 0) {
          domain_col_idx = k
          break
        }
      }
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
      next
    }

    # 정렬 행은 도메인 검증 skip
    if (is_align_row) next

    # 도메인 컬럼 값 검증 (표준 패턴 표만)
    if (needs_domain && domain_col_idx > 0) {
      n_cols = split(trimmed, dcols, /\|/)
      if (domain_col_idx <= n_cols) {
        validate_domain_cell(dcols[domain_col_idx], NR, line)
      }
    }
  }
}

END {
  if (errors > 0) {
    printf "\n표 형식 검증 실패: %d 건. 위 줄들을 확인해주세요.\n", errors
    exit 1
  } else {
    print "✓ 표 형식 검증 통과 — references/ko-ai-signals.md 의 모든 표가 정상 (4 컬럼 + 도메인 코드 valid)."
  }
}
' "$FILE"
