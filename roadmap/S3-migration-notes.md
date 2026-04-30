# S3 (v0.7 → v0.8) 마이그레이션 노트

> 이 문서는 v0.7 카탈로그를 직접 fork / inline 한 외부 사용자 / contributor 가 v0.8 로 올라올 때 참고할 수 있는 **breaking change 안내**다. 일반 사용자는 SKILL.md / PROMPT.md 만 새로 가져오면 끝.

---

## TL;DR

**v0.8 의 변경 한 줄**: 카탈로그 9 패턴 표가 **4 컬럼** (`나쁨 / 자연스러움 / 빈도 / 적용 도메인`) 으로 확장. **4 번째 customization mode** (Brand voice profile) 추가.

영향:

- **일반 사용자** (SKILL.md / PROMPT.md 만 사용): **영향 0** — 12 카테고리 / 정량 룰 / 출력 포맷 모두 동일. 4 번째 mode 는 *옵션*.
- **카탈로그를 직접 fork / 표 row 를 자기 도구에 inline 한 사용자**: **영향 있음** — 표 헤더가 3 컬럼 → 4 컬럼.
- **외부 lint / parser**: 4 컬럼 표 헤더 가정으로 갱신 필요.

---

## Breaking changes

### 1. 카탈로그 표 4 컬럼화 (필수 마이그레이션 영역)

**Before** (v0.7):

```markdown
| 나쁨 | 자연스러움 | 빈도 |
|---|---|---|
| 매우 중요한 | 중요한 / 꽤 중요한 | high |
```

**After** (v0.8):

```markdown
| 나쁨 | 자연스러움 | 빈도 | 적용 도메인 |
|---|---|---|---|
| 매우 중요한 | 중요한 / 꽤 중요한 | high | all |
```

영향 받는 카테고리: **#1, #2, #3, #4, #6, #7, #8, #11, #12** — 총 9 개 표, 약 110 행.

#### Fork 사용자 마이그레이션 절차

자기 fork 의 카탈로그가 v0.7 헤더라면:

1. 헤더 줄에 `| 적용 도메인 |` 컬럼 추가
2. 정렬 줄 (`|---|---|---|`) 에 `|---|` 한 칸 추가
3. 모든 데이터 행 끝에 도메인 값 추가:
   - **안전한 디폴트**: 모든 행 `| all |` 로 채움 (의미 변동 없음)
   - **선택적 specific 도메인**: high-priority 행만 도메인 코드 부여 (예: `marketing,review` / `formal` / `academic,wiki` 등). 부록 F 의 도메인 코드 표준 참조.

자동 마이그레이션 sed 한 줄 (모든 행 `all` 로):

```bash
# 카탈로그 9 표 모든 데이터 행 끝에 "all" 추가 (헤더 / 정렬 줄 제외)
# 주의: 카탈로그 외 다른 표 (부록 A.1 등) 도 손대므로 dry-run 권장
sed -i.bak -E '/^\|.*\|.*\|.*\|.*\|$/!{ /^\|.*\| (high|med|low) \|$/s/$/ all |/ }' references/ko-ai-signals.md
```

(실제 마이그레이션은 손으로 표 단위로 검토하는 게 안전. v0.8 본 레포의 카탈로그 자체가 reference.)

### 2. lint-patterns.sh v2 — 도메인 코드 검증 추가

기존 표 형식 검증 (`|` 개수 일치) 외에:

- 표준 패턴 표 (`나쁨` + `자연스러움` 헤더) 는 **`적용 도메인` 컬럼 의무**.
- "적용 도메인" 셀 값이 valid 도메인 코드인지 검증 — `all` / `informal` / `formal` / 12 개별 도메인 코드.
- `all` 과 다른 코드 혼용 금지 (`all` 은 단독).

**영향**: 자기 lint 도구가 `lint-patterns.sh` 를 fork 했다면 v2 로 갱신. 또는 v0.8 본 스크립트 그대로 가져다 쓰기 권장.

### 3. eval-harness — M5 (brand preserve) 옵션 metric 추가

- 기본 동작 변경 없음. fixture frontmatter 에 `brand_voice: <path>` 가 없으면 M5 = `n/a` (스킵).
- `brand_voice` 가 있고 brand voice 파일의 `preserve` 단어가 humanized 에 빠지면 M5 fail.
- scorecard 표에 M5 컬럼 추가. 외부 parser 가 scorecard 컬럼 수에 의존하면 갱신 필요.

---

## Non-breaking changes (안내만)

### Brand voice profile (4 번째 mode) — 선택 사용

- 기존 Personal list (방식 A/B/C) 와 *덧붙임* 으로 동작. 안 쓰면 v0.7 동작과 동일.
- 4 번째 mode 사용 시 적용 순서: **brand voice → personal list → 카탈로그**.

### 부록 F (도메인 코드 표준) 신설

- 카탈로그 부록 E 의 도메인 우선순위 매트릭스가 의존하는 도메인 코드 표준이 명문화.
- 새 도메인 추가 시 부록 F 에 행 + lint-patterns.sh 의 valid 셋 + 부록 E 우선순위 + `examples/domain-<new>.md` 사례까지 같이 갱신.

### `eval/frequency-data/` 스캐폴딩

- v0.8 첫 패스에는 데이터 미수집 (구조만). 카탈로그 빈도 라벨은 v0.7 의 휴리스틱 라벨 그대로 carry over.
- 후속 sub-PR (v0.8.1 또는 v0.9 후보) 에서 90 LLM 샘플 수집 → 빈도 재라벨링 PR 예정.
- 외부 사용자 영향: 빈도 라벨 자체는 v0.7 == v0.8 (재라벨링 안 했음). 후속 PR 시 변동 사유는 그 PR 에 명시.

---

## v1.0 freeze 약속과의 관계

S4 (v0.8 → v1.0) 에서 **카탈로그 v2 (4 컬럼) + brand voice 데이터 모델** 을 freeze 약속 대상에 포함. 즉 v1.0 부터:

- 카탈로그 4 컬럼 헤더 형식 고정 (`나쁨 / 자연스러움 / 빈도 / 적용 도메인` 순서·이름·개수)
- 도메인 코드 12 개 + shorthand 3 개 freeze (추가는 minor bump 가능, 제거 / 의미 변경은 major bump)
- Brand voice frontmatter 필드 (`name`, `domain_default`, `ending_default`, `preserve`, `ban`, `prefer` 의 7 핵심 필드) freeze
- `emoji_policy`, `length_bias` 같은 보조 필드는 v1.x minor 에서 추가 가능 (제거는 major)

따라서 v0.8 마이그레이션은 v1.0 직전 정합화의 마지막 큰 deformation 이고, v1.0 → v1.x 는 호환성 깨짐 없이 진행된다.

---

## 호환성 매트릭스

| 환경 | v0.7 → v0.8 영향 | 마이그레이션 필요? |
|---|---|---|
| Claude Code / OpenCode / Codex (skill 사용) | 0 | clone / pull 만 |
| Claude.ai (Cowork — SKILL.md 업로드) | 0 | 새 SKILL.md 다시 업로드 |
| ChatGPT / Cursor / Gemini (PROMPT.md 시스템 프롬프트) | 0 | 새 PROMPT.md 로 갱신 |
| 카탈로그 fork / inline | 큼 | 4 컬럼 헤더 + 도메인 코드 부여 |
| 외부 lint 도구 fork | 중간 | lint-patterns.sh v2 로 갱신 또는 본 스크립트 사용 |
| 외부 eval-harness fork | 중간 | M5 metric 무시하거나 옵션으로 수용 |

---

## 변경 사유 / 디자인 결정 요약

- **4 컬럼 vs 별도 weight 매트릭스**: 4 컬럼 채택. single source of truth (카탈로그 자체) 유지, lint 단순.
- **shorthand (`all` / `informal` / `formal`)**: 표를 짧게 유지. `all` 은 단독, 나머지는 다른 코드와 결합 가능.
- **데이터 기반 빈도 재라벨링 분리**: 90 샘플 수집은 시간 소요 큼 → S3 spec 의 task 2D 는 **방법론 / 스캐폴딩까지** 만 v0.8 에 포함, 실 데이터 수집은 sub-PR 분리. v1.0 freeze 에 영향 없음.
- **Brand voice = personal list 의 superset?**: 의도적으로 **별도 mode**. Personal list 는 단어 리스트 (3-5 줄로 끝남), brand voice 는 frontmatter + 톤 가이드로 풍부함. 같은 개념을 두 깊이로 운용.
- **케이스 스터디 2 개의 의도적 대비**: Toss 풍 (concise / ~해요) vs 작가 X (verbose / ~다) — 같은 humanizer 가 brand voice 만으로 두 끝점 모두 생산할 수 있음을 보여줌.

---

## 후속 작업 (S4 또는 v0.8.x sub-PR)

- [ ] `eval/frequency-data/` 90 샘플 수집 → 137 패턴 빈도 카운팅 → 카탈로그 라벨 갱신 PR
- [ ] Brand voice 자동 추출 도구 (사용자 글 샘플 → brand voice frontmatter 생성) — v1.x 후보
- [ ] LLM-as-judge brand voice 일관성 평가 metric — v1.x 후보
- [ ] 추가 도메인 (`podcast` / `lecture` / `x-thread`) — v1.x minor
- [ ] 카테고리 #13+ — 실 사용 데이터 기반 필요 시 (major bump 동반)

S4 (v1.0 stabilization) 는 위 작업들 모두 v1.x 트랙으로 미루고 **v0.8 의 surface freeze + 베타 + 안정화** 만 한다.
