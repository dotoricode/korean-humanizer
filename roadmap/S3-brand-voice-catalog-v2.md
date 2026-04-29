# Sprint 3 — v0.8 Brand Voice + Catalog v2

> Personal list 의 4 번째 mode (brand voice profile) 도입 + 카탈로그를 도메인-가중치 기반 4 컬럼으로 재구성. v1.0 직전의 가장 큰 깊이 점프.

| 항목 | 값 |
|---|---|
| 버전 | v0.7 → v0.8 |
| 기간 | 3 주 (15 working days) |
| 의존 | S1 eval-harness + S2 도메인 셋 |
| 외부 의존 | 없음 (가상 brand 케이스만) |
| 위험도 | **중간** (137 행 재라벨링 + brand voice 디자인 실수 위험) |
| 다음 sprint | S4 v1.0 안정화 — 이번 sprint 의 카탈로그 v2 가 freeze 대상 |

---

## Goal 1 — Brand Voice Profile (4 번째 customization mode)

humanizer 가 사용자 *브랜드 톤* 을 선반영할 수 있게 한다. 현재는 일반적 한국어 LLM 톤 기준 12 카테고리만 → "Toss 풍 / 직설 풍 / 작가 X 톤" 같은 톤 프로필을 사용자가 정의할 수 있게.

## Goal 2 — Catalog v2 (도메인-가중치 4 컬럼)

빈도 컬럼을 도메인별 컨텍스트와 결합. 같은 패턴이라도 마케팅에서는 high, 이메일에서는 med 인 차이를 표현.

---

## Why

- **사용자 톤 다양성**: "humanize 가 너무 평범하게 만든다 / 우리 회사 톤이 아니다" 는 가장 자주 받을 피드백. 4 번째 mode 가 이를 해결.
- **카탈로그 정밀도**: "활용" 은 마케팅에서는 catch 해야 하지만 학술 초록에서는 의도된 격식어. 도메인 컬럼이 있어야 정확한 적용.
- **v1.0 안정화 약속의 기반**: 카탈로그 v2 가 freeze 약속의 대상. v0.8 까지 정리해야 v1.0 에서 약속 가능.

---

## Deliverables

### Part 1 — Brand Voice

| 산출물 | 경로 | 설명 |
|---|---|---|
| Brand voice 템플릿 | `examples/brand-voice-template.md` | 보존어 / 금지어 / 선호 매핑 / 톤 가이드 / 도메인 디폴트 통합 |
| 케이스 스터디 1 | `examples/brand-voice-toss-style.md` | 가상 핀테크 — 짧고 직설, 친근 격식 최소화 |
| 케이스 스터디 2 | `examples/brand-voice-essayist.md` | 가상 작가 — 길고 사변, 1 인칭, 비유 |
| SKILL.md 4 번째 mode | 방식 D 섹션 | Brand voice 적용 방법, 우선순위, 호환성 |
| PROMPT.md 4 번째 mode | personal list 섹션 확장 | 동일 |

### Part 2 — Catalog v2

| 산출물 | 경로 | 설명 |
|---|---|---|
| 카탈로그 v2 | `references/ko-ai-signals.md` | `\| 나쁨 \| 자연스러움 \| 빈도 \| 적용 도메인 \|` 4 컬럼 |
| 도메인 컬럼 값 표준 | 카탈로그 부록 F | "all" / "blog,marketing" 등 도메인 코드 |
| 빈도 재라벨링 | 카탈로그 빈도 컬럼 | 데이터 기반 (LLM 출력 샘플링) |
| lint-patterns.sh v2 | `scripts/lint-patterns.sh` | 4 컬럼 검증 + 도메인 코드 valid 검증 |
| 마이그레이션 노트 | `roadmap/S3-migration-notes.md` | 0.7 → 0.8 호환성 (외부 fork 가 있다면) |

---

## Tasks

### Part 1 — Brand Voice (5d)

#### 1A. Brand voice 데이터 모델 디자인 (1d)

결정해야 할 것:

- **포맷**: markdown frontmatter + 본문 vs YAML 단독 vs JSON
  - **결정**: markdown frontmatter (이미 fixture 와 호환), 본문에는 톤 가이드 자유 기술
- **필수 필드**: `name`, `domain_default`, `preserve` (보존어), `ban` (금지어), `prefer` (선호 매핑), `tone_guide`
- **선택 필드**: `ending_default` (~합니다 / ~해요 / ~다 / 반말), `emoji_policy` (none / sparse / liberal), `length_bias` (concise / verbose)
- **적용 순서** (확정):
  1. Brand voice (있으면 가장 우선)
  2. Personal list (Mode A/B/C)
  3. 12 카테고리 카탈로그 (도메인-가중치 적용)

#### 1B. Brand voice 템플릿 (1d)

`examples/brand-voice-template.md`:

```markdown
---
name: my-brand
domain_default: blog
ending_default: ~다
emoji_policy: sparse
length_bias: concise
preserve:
  - "딥다이브"
  - "프로덕트 마켓 핏"
ban:
  - "활용"
  - "혁신적인"
prefer:
  - "사용 → 쓰기"
  - "유용하다 → 쓸만하다"
---

## Tone guide (자유 기술)

- 1 문장 8-15 자 권장.
- 강조는 단어가 아니라 문장 길이로.
- 인사·마무리 말은 의도된 자리에만.
```

#### 1C. 케이스 스터디 1 — Toss 풍 핀테크 (1.5d)

가상 핀테크 스타트업 brand voice:

- preserve: "쉽게", "빠르게", "간편하게"
- ban: "혁신", "활용", "극대화", "체계적"
- 톤: 짧고 친근, 격식 최소화, 이모지 없음
- raw → humanized 사례 3 개 (블로그 / 앱 카피 / 이메일)

#### 1D. 케이스 스터디 2 — 작가 X 톤 (1.5d)

가상 에세이스트 brand voice:

- preserve: 작가 특유 표현 ("문득", "결국엔")
- ban: AI 톤 일반 ("다양한", "혁신적인")
- 톤: 길고 사변, 1 인칭, 비유 사용
- ending_default: ~다
- raw → humanized 사례 2 개 (에세이 단편)

### Part 2 — Catalog v2 (10d)

#### 2A. 카탈로그 v2 디자인 (1d)

- **결정 1**: 4 컬럼 vs 별도 weight 매트릭스
  - **결정**: 4 컬럼 (single source of truth 유지, lint 단순)
- **결정 2**: 도메인 컬럼 값 형식
  - **결정**: 콤마 리스트 또는 "all" (예: `marketing,review` / `all`)
- **결정 3**: 어느 행이 specific 도메인을 받고, 어느 행이 "all" 인가
  - **결정**: 카테고리 #1 (강조어) 처럼 보편 패턴은 "all". 카테고리 #11 (hedging) 처럼 도메인별 차이 큰 패턴은 specific.
- 도메인 코드 (부록 F 표준):
  ```
  all = blog, marketing, email, linkedin, youtube, newsletter, wiki,
        academic, news, chat, review, b2b-message
  ```
  shorthand: `informal = chat,review`, `formal = email,b2b-message,academic`

#### 2B. 카탈로그 v2 마이그레이션 — 137 행 4 컬럼화 (3d)

- 카테고리 #1-#4, #6-#8, #11, #12 의 9 표 (~110 행) 4 컬럼 확장
- 첫 패스: 모든 행 `all` 부여 (안전 디폴트)
- 두 번째 패스: high-priority ~30 행에 specific 도메인 부여
  - 예: "혁신적인 솔루션" → `marketing,review` (마케팅·리뷰 빈출)
  - 예: "고려되어야 합니다" → `formal` (격식 도메인 빈출)
- 나머지 ~80 행은 `all` 유지

#### 2C. lint-patterns.sh v2 (1d)

추가 검증:

- 표 헤더에 "빈도" + "적용 도메인" 모두 포함
- 도메인 컬럼 값이 valid 도메인 코드인지 (`all`, `informal`, `formal`, 또는 콤마-구분 known 도메인)
- 도메인 코드 unknown 시 fail + 가능한 후보 출력

#### 2D. 빈도 재라벨링 — 데이터 기반 (3d, 가장 무거움)

- **데이터 수집** (1.5d):
  - Claude / GPT / Gemini 각 30 prompts (블로그 / 마케팅 / 이메일 / LinkedIn / 뉴스레터 도메인 6 개씩)
  - prompt 는 humanizer 의식 없이 평소 한국어 출력 유도
  - 각 모델 × 각 prompt = 90 출력 샘플
- **빈도 측정** (1d):
  - 카탈로그 137 패턴 각각의 출현 횟수 카운트 (grep / regex)
  - 출현률 = 출현 sample 수 / 90
  - high: 출현률 ≥ 30 %, med: 5-30 %, low: < 5 %
- **재라벨링** (0.5d):
  - 현재 "high" 약 30 개 → 데이터로 검증, 변동 PR 으로 명시
  - 새 "low" 발견 시 카탈로그에 명시
- 데이터 raw 는 `eval/frequency-data/` 에 보관 (재현용, gitignore 안 함)

#### 2E. SKILL/PROMPT 4 번째 mode 통합 (1d)

- SKILL.md "사용자 커스터마이징" 섹션 확장:
  - 방식 D. Brand voice profile (Mode A/B/C 보다 *우선*)
- PROMPT.md "개인 금지어 / 선호어" 섹션 확장
- 적용 순서 명시: Brand voice → Personal list → 카탈로그

#### 2F. lint-cross-file.sh brand voice 검증 (선택, 0.5d)

- 두 케이스 스터디 brand voice 가 SKILL/PROMPT 의 4 번째 mode 설명과 sync 되는지

#### 2G. eval-harness 갱신 (0.5d)

- Brand voice 가 적용된 fixture 도 eval 통과해야 함
- M1-M4 그대로, brand voice 의 보존어가 humanized 에 보존됐는지 확인하는 옵션 metric 추가 검토 (선택)

### 마무리 (1d)

- README 갱신: brand voice mode 소개, 카탈로그 v2 변경 한 줄 알림
- CONTRIBUTING.md 갱신: 4 번째 컬럼 (도메인) 분류 가이드
- v0.8 GitHub release notes (breaking change 명시: 카탈로그 표 4 컬럼)
- ROADMAP.md S3 status 갱신

---

## Acceptance criteria

### Brand voice

- [ ] 템플릿 + 2 케이스 스터디 완성
- [ ] SKILL/PROMPT 4 번째 mode 통합
- [ ] 적용 순서 명시 (brand → personal → 카탈로그)

### Catalog v2

- [ ] 137 행 모두 4 컬럼 (`나쁨 / 자연스러움 / 빈도 / 적용 도메인`) 채워짐
- [ ] high-priority 30 행은 specific 도메인 부여
- [ ] 빈도 컬럼 데이터 기반 재라벨링 완료
- [ ] 데이터 raw 가 `eval/frequency-data/` 에 보관됨
- [ ] lint-patterns.sh v2 가 4 컬럼·도메인 코드 검증
- [ ] lint-cross-file 통과

### 통합

- [ ] 모든 lint 4 종 + eval-harness 통과
- [ ] v0.8 GitHub release tag (CHANGELOG 에 breaking change 명시)

---

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| 137 행 재라벨링 시간 over-run | 첫 패스는 모두 `all` 부여 후 high-priority 30 행만 specific. 나머지는 후속 PR. |
| LLM 샘플링 데이터 수집이 시간 소요 큼 | 모델 3 개 × 30 prompts = 90 샘플로 시작. 부족하면 후속 sprint 에서 확장. |
| Brand voice 디자인 실수 (호환성 깨짐) | Personal list Mode A/B/C 와 *덧붙임* 으로만 동작. 기존 사용자 업그레이드 시 영향 0. |
| 4 컬럼 표가 모바일 GitHub 에서 너무 좁아짐 | 컬럼 너비 표준화, Wiki 링크로 풀 버전 안내 |
| 빈도 재라벨링이 기존 "high" 와 큰 차이 (혼란) | PR 에 변동 사유 명시, 일부는 보수적으로 유지 |

---

## Out of scope

- 실제 기업 brand voice (가상 케이스만 사용)
- LLM-as-judge brand voice 일관성 평가 (다음 라운드)
- Brand voice 자동 생성 도구 (사용자가 수동으로 채움)
- 다국어 brand voice (out-of-scope, 영구 — 한국어 전용)
- X·Threads / 강의 도메인 (S2 에서 미루었으면 후속 PR)

---

## Effort breakdown

| Task | 시간 |
|---|---|
| **Part 1 — Brand voice** | **5d** |
| 1A. 데이터 모델 디자인 | 1d |
| 1B. 템플릿 | 1d |
| 1C. 케이스 스터디 1 (Toss 풍) | 1.5d |
| 1D. 케이스 스터디 2 (작가 X) | 1.5d |
| **Part 2 — Catalog v2** | **9d** |
| 2A. 카탈로그 v2 디자인 | 1d |
| 2B. 137 행 4 컬럼화 | 3d |
| 2C. lint-patterns.sh v2 | 1d |
| 2D. 빈도 재라벨링 (데이터) | 3d |
| 2E. SKILL/PROMPT 4 번째 mode | 1d |
| 마무리 (release / docs / 회고) | 1d |
| **합계** | **15d (3 주)** |

Buffer 1-2d 권장 (재라벨링 시간 over-run 가능).
