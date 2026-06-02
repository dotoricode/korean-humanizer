#!/usr/bin/env bash
# Cross-file sync 검증 — SKILL.md / PROMPT.md / references/ko-ai-signals.md
# 사일런트 드리프트(한 파일만 바뀌고 나머지가 안 바뀜) 방지.
#
# 검증 항목:
#   1. 정량 규칙(20%, 3곳, 90%) 이 세 파일에 모두 등장하는지
#   2. 12 카테고리 키워드가 세 파일에 모두 등장하는지
#   3. 카테고리 #13 이상이 추가되지 않았는지 (12 + 합의된 확장만 허용)
#
# 실패 시 어느 파일에서 빠졌는지 출력 후 exit 1.
#
# 사용법:
#   bash scripts/lint-cross-file.sh

set -euo pipefail

FILES=(
  "SKILL.md"
  "PROMPT.md"
  "references/ko-ai-signals.md"
)

# 카테고리별 sync 키워드 — 카테고리 이름의 핵심어 하나씩.
# 세 파일에 모두 등장해야 한다. 정확한 표기 차이(예: "이모지 남발" vs "이모지 / 이모티콘 남발")는 허용,
# 핵심 키워드 부재만 catch.
CATEGORIES=(
  "강조어"        # 1. Empty intensifiers
  "공허"          # 2. Empty adjectives
  "번역체"        # 3. Translation-ese
  "것이다"        # 4. "것이다 / 이러한 / 해당"
  "판에 박"       # 5. Formulaic openings/closings
  "수동"          # 6. Passive
  "연결어"        # 7. Filler connectives
  "parallelism"   # 8. Forced parallelism
  "존댓말"        # 9. Honorific mismatch
  "이모지"        # 10. Emoji overuse
  "hedging"       # 11. Hedging
  "고빈도"        # 12. AI vocab
)

# 정량 규칙 — 세 파일 모두에 등장해야 함.
# 한 파일에서만 바뀌면 lint fail (예: SKILL 만 25% 로 바뀌고 PROMPT/카탈로그는 20% 인 경우).
QUANT_RULES=(
  "20%"
  "3곳"
  "90%"
)

errors=0

# 0. 파일 존재 확인
for file in "${FILES[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "FAIL: $file 파일이 없습니다."
    errors=$((errors + 1))
  fi
done

if [[ $errors -gt 0 ]]; then
  exit 1
fi

# 1. 정량 규칙 sync
for rule in "${QUANT_RULES[@]}"; do
  for file in "${FILES[@]}"; do
    if ! grep -qF "$rule" "$file"; then
      echo "FAIL: 정량 규칙 '$rule' 가 $file 에 없습니다 — 다른 두 파일과 sync 가 깨졌습니다."
      errors=$((errors + 1))
    fi
  done
done

# 2. 카테고리 키워드 sync
for i in "${!CATEGORIES[@]}"; do
  cat_num=$((i + 1))
  keyword="${CATEGORIES[$i]}"
  for file in "${FILES[@]}"; do
    if ! grep -qF "$keyword" "$file"; then
      echo "FAIL: 카테고리 #$cat_num 키워드 '$keyword' 가 $file 에 없습니다."
      errors=$((errors + 1))
    fi
  done
done

# 3. 13 번 카테고리 미허용 체크
for file in "${FILES[@]}"; do
  if grep -Eq "^#{2,3}[[:space:]]+13\." "$file"; then
    echo "FAIL: $file 에 카테고리 #13 이상이 있습니다. 12 + 합의된 확장만 허용."
    errors=$((errors + 1))
  fi
done

# 4. Brand voice (방식 D / 형식 D) sync — SKILL 과 PROMPT 양쪽에 모두 등장해야 함
if ! grep -qF "방식 D" SKILL.md; then
  echo "FAIL: Brand voice 키워드 '방식 D' 가 SKILL.md 에 없습니다 — 4 번째 mode (Brand voice profile) sync 가 깨졌습니다."
  errors=$((errors + 1))
fi
if ! grep -qF "형식 D" PROMPT.md; then
  echo "FAIL: Brand voice 키워드 '형식 D' 가 PROMPT.md 에 없습니다 — 4 번째 mode (Brand voice profile) sync 가 깨졌습니다."
  errors=$((errors + 1))
fi

# 5. Brand voice 템플릿·케이스 스터디 파일 존재 확인
BRAND_FILES=(
  "examples/brand-voice-template.md"
  "examples/brand-voice-toss-style.md"
  "examples/brand-voice-essayist.md"
)

for bf in "${BRAND_FILES[@]}"; do
  if [[ ! -f "$bf" ]]; then
    echo "FAIL: Brand voice 파일 '$bf' 가 없습니다 — SKILL/PROMPT 의 4 번째 mode 가 가리키는 레퍼런스가 빠졌습니다."
    errors=$((errors + 1))
  fi
done

# 6. 도메인 코드 부록 F sync — 카탈로그에 부록 F 가 있어야 함 (v0.8 카탈로그 v2 의 lint 의존)
if ! grep -qF "부록 F. 도메인 코드 표준" "references/ko-ai-signals.md"; then
  echo "FAIL: 카탈로그에 '부록 F. 도메인 코드 표준' 이 없습니다 — lint-patterns.sh v2 가 이 부록을 valid 도메인 셋의 single source of truth 로 합니다."
  errors=$((errors + 1))
fi

if [[ $errors -gt 0 ]]; then
  echo ""
  echo "Cross-file sync 검증 실패: $errors 건."
  echo "SKILL.md / PROMPT.md / references/ko-ai-signals.md 세 파일의 정량 규칙·카테고리·4 번째 mode (Brand voice) sync 를 확인하세요."
  exit 1
fi

echo "✓ Cross-file sync 검증 통과 — SKILL/PROMPT/카탈로그의 정량 규칙(20%/3곳/90%) · 12 카테고리 키워드 · 4 번째 mode (Brand voice) · 부록 F 가 모두 일치."
