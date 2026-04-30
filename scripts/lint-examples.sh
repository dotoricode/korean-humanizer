#!/usr/bin/env bash
# Examples integrity 검증 — examples/*.md 가 SKILL 출력 포맷·카탈로그 범위를 따르는지.
#
# 검증 항목:
#   1. "주요 변경 (최대 5개)" 섹션의 후속 bullet 항목 개수 ≤ 5
#   2. 카테고리 번호 참조가 1~12 범위인지 (#13 이상 금지)
#   3. (v0.8) examples/brand-voice-*.md frontmatter 7 핵심 필드 + valid 값
#
# 통과 시 examples/ 가 SKILL.md 의 출력 포맷 룰을 위반하지 않는다는 보증.
#
# 사용법:
#   bash scripts/lint-examples.sh

set -euo pipefail

EXAMPLES_DIR="examples"

if [[ ! -d "$EXAMPLES_DIR" ]]; then
  echo "ERR: $EXAMPLES_DIR 디렉토리가 없습니다."
  exit 1
fi

errors=0

# Check 1: "주요 변경 (최대 5개)" 섹션 ≤ 5 bullet
# 다음 헤딩이 나올 때까지 bullet 카운트.
for file in "$EXAMPLES_DIR"/*.md; do
  awk -v file="$file" '
    BEGIN {
      in_section = 0
      heading_line = 0
      bullet_count = 0
      err = 0
    }

    function flush() {
      if (in_section && bullet_count > 5) {
        printf "FAIL %s:%d \"주요 변경 (최대 5개)\" 섹션에 %d 개 항목 — 5 이하여야 합니다.\n",
          file, heading_line, bullet_count
        err = 1
      }
      in_section = 0
      bullet_count = 0
    }

    /^#{2,4}.*주요 변경.*최대 5개/ {
      flush()
      in_section = 1
      heading_line = NR
      bullet_count = 0
      next
    }

    in_section && /^#{1,6}[[:space:]]/ {
      flush()
      next
    }

    in_section && /^[[:space:]]*[-*][[:space:]]/ {
      bullet_count++
    }

    END {
      flush()
      exit err
    }
  ' "$file" || errors=$((errors + 1))
done

# Check 2: 카테고리 번호 #13 이상 금지
# "#13", "#14" ... "#99" 패턴 발견 시 fail. "카테고리 13" 도 catch.
for file in "$EXAMPLES_DIR"/*.md; do
  bad_lines=$(grep -nE "(#|카테고리[[:space:]]*)(1[3-9]|[2-9][0-9])([^0-9%]|$)" "$file" || true)
  if [[ -n "$bad_lines" ]]; then
    echo "FAIL: $file 에 카테고리 #13 이상 참조가 있습니다 (1~12 만 허용):"
    echo "$bad_lines"
    errors=$((errors + 1))
  fi
done

# Check 3: brand voice frontmatter 7 핵심 필드 + valid 값 (v0.8 카탈로그 v2)
# 7 핵심 필드 = name / domain_default / ending_default / preserve / ban / prefer / length_bias
# domain_default 는 12 개별 도메인 코드 (shorthand 안 됨 — 한 brand voice = 한 디폴트)
# ending_default 는 ~합니다 / ~해요 / ~다 / 반말 / auto

VALID_DOMAINS_INDIVIDUAL="blog marketing email linkedin youtube newsletter wiki academic news chat review b2b-message"
VALID_ENDINGS="~합니다 ~해요 ~다 반말 auto"
BRAND_REQUIRED_FIELDS="name domain_default ending_default preserve ban prefer length_bias"

for file in "$EXAMPLES_DIR"/brand-voice-*.md; do
  [[ -f "$file" ]] || continue

  # Extract frontmatter (between first two `---` lines)
  fm=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$file")
  if [[ -z "$fm" ]]; then
    echo "FAIL: $file frontmatter (--- ... ---) 가 없습니다."
    errors=$((errors + 1))
    continue
  fi

  # 7 필수 필드 모두 존재
  for field in $BRAND_REQUIRED_FIELDS; do
    if ! grep -qE "^${field}:" <<<"$fm"; then
      echo "FAIL: $file frontmatter 에 필수 필드 '${field}:' 가 없습니다."
      errors=$((errors + 1))
    fi
  done

  # domain_default valid 값
  domain_value=$(grep -E "^domain_default:" <<<"$fm" | head -1 | sed -E 's/^domain_default:[[:space:]]*([^[:space:]]+).*$/\1/')
  if [[ -n "$domain_value" ]]; then
    valid=0
    for d in $VALID_DOMAINS_INDIVIDUAL; do
      if [[ "$domain_value" == "$d" ]]; then
        valid=1
        break
      fi
    done
    if [[ $valid -eq 0 ]]; then
      echo "FAIL: $file domain_default='$domain_value' 가 valid 도메인 코드가 아닙니다."
      echo "       valid: $VALID_DOMAINS_INDIVIDUAL"
      errors=$((errors + 1))
    fi
  fi

  # ending_default valid 값
  ending_value=$(grep -E "^ending_default:" <<<"$fm" | head -1 | sed -E 's/^ending_default:[[:space:]]*([^[:space:]]+).*$/\1/')
  if [[ -n "$ending_value" ]]; then
    valid=0
    for e in $VALID_ENDINGS; do
      if [[ "$ending_value" == "$e" ]]; then
        valid=1
        break
      fi
    done
    if [[ $valid -eq 0 ]]; then
      echo "FAIL: $file ending_default='$ending_value' 가 valid 종결어미가 아닙니다."
      echo "       valid: $VALID_ENDINGS"
      errors=$((errors + 1))
    fi
  fi
done

if [[ $errors -gt 0 ]]; then
  echo ""
  echo "Examples integrity 검증 실패: $errors 건."
  echo "examples/ 의 \"주요 변경 (최대 5개)\" 항목 수, 카테고리 번호 범위, brand voice frontmatter 를 확인하세요."
  exit 1
fi

echo "✓ Examples integrity 검증 통과 — 5개 룰 + 카테고리 범위(1~12) + brand voice frontmatter 모두 정상."
