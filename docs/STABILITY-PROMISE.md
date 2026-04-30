# Stability Promise (v1.0+)

> `korean-humanizer` 1.0 부터 [SemVer](https://semver.org/) 를 따른다. 사용자 / contributor 가 룰이 갑자기 바뀌는 걱정 없이 의존할 수 있도록, 어떤 영역이 freeze 되고 어떤 영역이 minor / patch 로 바뀔 수 있는지 명문화한다.

---

## TL;DR

- **1.x.x** 동안 깨지지 않는 surface (아래 §Freeze 영역) 에 의존해도 OK.
- **카테고리 / 출력 포맷 / 정량 룰 / 카탈로그 표 헤더 / Brand voice 핵심 필드** = freeze.
- **카탈로그 패턴 행 / 도메인 추가 / 자연스러움 컬럼 개선 / 빈도·도메인 재라벨링** = minor (1.x.0).
- **lint / CI 인프라 / 오탈자** = patch (1.0.x).
- **위 freeze 영역 변경** = major (2.0.0).

---

## Freeze 영역 (1.x 동안 깨지지 않음)

### 1. 12 카테고리 구조

| 항목 | freeze 내용 |
|---|---|
| 카테고리 개수 | **12 개 고정**. 추가 / 삭제 / 번호 변경은 **major (2.0)**. |
| 카테고리 라벨 | "강조어 남발 / 공허한 형용사 / 과격식·번역체 / 것이다·이러한·해당 / 판에 박힌 개시·마무리 / 수동태·모호한 주어 / 불필요한 연결어 / 과도한 parallelism·3항 나열 / 존댓말 레벨 불일치 / 이모지 남발 / 단정 회피·hedging / AI 고빈도 어휘" — 이 12 라벨은 의미 동일하게 유지. 표기 미세 조정은 patch OK. |
| 9-A 발화체 ~다체 금지 | 핵심 룰. 1.x 유지. |

### 2. SKILL.md 출력 포맷

```
## Humanized

[다듬어진 텍스트 전체]

## 주요 변경 (최대 5개)
- "X" → "Y" (이유: ...)

(변경이 5개를 초과하면 마지막 줄에 "+N개 더 — '전체 diff로 보여줘'라고 하면 모두 표시")
```

- `## Humanized` + `## 주요 변경 (최대 5개)` 두 섹션 구조 유지.
- "최대 5개" 는 freeze. 늘리거나 줄이지 않음.
- 변경 5개 초과 시 `+N개 더` 안내 한 줄 포맷 freeze.
- 첫 응답에 한 번 붙는 마무리 안내 (`*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*`) freeze. 표현 개선 (예: 한국어 어색함 수정) 은 patch OK.

### 3. 정량 규칙

| 룰 | freeze 값 |
|---|---|
| 한 문단 수정 cap | **3 곳** |
| 전체 문장 수정 cap | **20 %** |
| 발화체 도메인 ~다체 글말체 | **금지** |
| Personal list 적용 순서 | brand voice → personal list → 카탈로그 |

이 4 개 정량 룰은 SKILL.md / PROMPT.md / 카탈로그 / lint-cross-file.sh 모두에 같은 표현. 1.x 유지. 변경 시 major bump.

### 4. PROMPT.md API

- 시스템 프롬프트로 **그대로 붙여 쓸 수 있는** 형식 유지 (외부 LLM 사용자 호환성).
- 12 카테고리 / 정량 룰 / 출력 형식 / 4 mode (A/B/C/D) 구조 유지.
- 환경별 안내 (ChatGPT / Cursor / Gemini / 기타) 추가는 minor OK.

### 5. 카탈로그 4 컬럼 표 헤더

```
| 나쁨 | 자연스러움 | 빈도 | 적용 도메인 |
```

- 컬럼 순서 / 이름 / 개수 = freeze.
- 새 컬럼 추가는 major (외부 fork / parser 가 깨짐).

### 6. 도메인 코드 표준 (부록 F)

| 항목 | freeze 내용 |
|---|---|
| 12 개별 도메인 코드 | `blog` / `marketing` / `email` / `linkedin` / `youtube` / `newsletter` / `wiki` / `academic` / `news` / `chat` / `review` / `b2b-message` — 코드명 / 의미 freeze. |
| Shorthand 3 개 | `all` / `informal` (= chat,review) / `formal` (= email,b2b-message,academic) — freeze. |
| 컬럼 값 작성 룰 | `all` 단독 / 콤마 구분 / shorthand 정확 매칭 시 사용 / `all` 과 다른 코드 혼용 금지 — freeze. |

새 도메인 코드 추가는 minor (1.x.0). 기존 코드 의미 변경 / 제거는 major (2.0).

### 7. Brand voice 7 핵심 필드

```yaml
name: <string>
domain_default: <도메인 코드>
ending_default: ~합니다 / ~해요 / ~다 / 반말 / auto
preserve: [<word>, ...]
ban: [<word>, ...]
prefer: ["A → B", ...]
length_bias: concise / neutral / verbose
```

- 이 7 필드는 1.x 동안 의미 / 동작 freeze.
- 새 필드 추가 (예: `tone_examples`, `register`) 는 minor — 기존 7 필드 무시 안 함.
- 7 필드 의미 변경 / 제거 = major.

`emoji_policy` 등 보조 필드는 v0.8 부터 있지만 **non-core** — minor 에서 변경 가능 (예: `none/sparse/liberal` 외 값 추가, 의미 미세 조정).

### 8. Personal list Mode A/B/C/D

| Mode | freeze 내용 |
|---|---|
| A 인라인 한 줄 | `금지=...; 선호=A→B; 유지=...` 형식 freeze. 키 별칭 (`ban` / `avoid` / `prefer` / `keep`) freeze. |
| B 자연어 한 줄 | "X 빼고, Y 는 Z 로" 류 자연어 파싱 — 정확한 grammar 는 휴리스틱이라 freeze 못 하지만, **자연어 입력이 받아들여진다** 는 약속은 freeze. |
| C 파일 | `examples/personal-list.md` + `SKILL.md` 의 `## My personal list` 섹션 - 두 진입 모두 freeze. |
| D Brand voice | `examples/brand-voice-*.md` frontmatter (위 §7) + 자유 톤 가이드 본문 - 입력 형식 freeze. |

### 9. 정량 메트릭 M1-M5

eval-harness 의 metric 5 종 (`M1` 수정 비율, `M2` 단락 cap, `M3` 길이 비율, `M4` ~다체 보존, `M5` brand preserve) — 1.x 유지. 새 metric 추가는 minor (옵션 metric 으로). 기존 metric 의미 변경 / 제거 = major.

---

## Minor (1.x.0) 허용 변경

freeze 영역을 깨지 않으면서 다음은 minor 에서 추가 / 개선:

- ✓ 카탈로그 137 패턴 행 추가 / 자연스러움 컬럼 개선 (의미 동일).
- ✓ 빈도 컬럼 데이터 기반 재라벨링 (high → med 같은 라벨 변경, 패턴 자체 유지).
- ✓ 적용 도메인 컬럼 재라벨링 (`all` → `marketing,review` 같은 specific 화).
- ✓ 새 도메인 추가 (예: `podcast`, `lecture`, `x-thread`) — 부록 F + lint + examples 동시 갱신 의무.
- ✓ 새 examples 사례 추가 (`examples/domain-*.md`, `examples/brand-voice-*.md`).
- ✓ Brand voice 보조 필드 추가 (예: `tone_examples`, `register`).
- ✓ 새 옵션 metric (M6+) 추가 — fixture frontmatter 옵션 필드로 활성화.
- ✓ 환경별 설치 가이드 추가 (예: 새 LLM 도구 출시 시).
- ✓ 문서 / README / 다이어그램 개선.
- ✓ Eval fixture 추가 (eval/fixtures/, eval/frequency-data/).

---

## Patch (1.0.x) 허용 변경

- ✓ 오탈자 / 문법 수정.
- ✓ lint 룰 미세 조정 (false positive / negative 수정).
- ✓ CI 인프라 변경 (workflow 업데이트, runner 버전 등).
- ✓ Test fixture 안정화 (의도되지 않은 flake 해결).
- ✓ Brand voice 케이스 스터디 본문 표현 개선 (frontmatter freeze).

---

## Breaking → 2.0.0

다음은 **major bump** 동반:

- 위 freeze 영역 (§1-9) 변경.
- 카테고리 #13 추가 / 삭제 / 번호 재배치.
- 정량 룰 cap 값 변경 (20% → 25% 같은).
- 카탈로그 표 헤더 컬럼 추가 / 제거 / 순서 변경.
- 도메인 코드 의미 변경 / 제거.
- Brand voice 7 핵심 필드 의미 변경 / 제거.
- Personal list Mode A 인라인 grammar 변경.

Major bump 시 의무:

1. **마이그레이션 가이드 동봉** (`docs/MIGRATION-1.x-to-2.x.md`).
2. **CHANGELOG 에 BREAKING 명시**.
3. **N-1 메이저 (1.x) 보안 패치 12 개월 지원** — 즉시 cutoff 금지.
4. **공지** — README hero + GitHub release notes + 기존 의존 사용자 알림.

---

## 호환성 매트릭스 — 1.x 의존 사용자 영향

| 환경 | 1.0 → 1.x.x 영향 |
|---|---|
| Claude Code / OpenCode / Codex (skill 사용) | **영향 0** — pull / clone 만으로 자동 적용. |
| Claude.ai (Cowork — SKILL.md 업로드) | minor 시 SKILL.md 다시 업로드 권장. patch 는 무시 OK. |
| ChatGPT / Cursor / Gemini (PROMPT.md 시스템 프롬프트) | 동일 — minor 시 갱신 권장. |
| 카탈로그 fork / inline | minor 에서 새 패턴 행 / 도메인 추가 가능 — fork 가 모든 행을 inline 했다면 cherry-pick 필요. |
| 외부 lint / parser fork | minor 시 valid 도메인 셋 / 카탈로그 표 추가 행 sync — 일반적으로 자동. |
| 외부 eval-harness fork | minor 에서 옵션 M6+ 추가 가능 — 무시하면 1.0 동작 유지. |

---

## v1.0 이후 후속 후보 (1.x minor 트랙)

`korean-humanizer` 1.0 출시 후 다음 트랙으로 minor / sub-PR 검토:

- **빈도 데이터 재라벨링** (v1.0.x or v1.1) — 90 LLM 샘플 (`eval/frequency-data/`) 기반 137 패턴 빈도 재산정.
- **추가 도메인** (v1.x) — `podcast` / `lecture` / `x-thread` 같은 발화체 / 짧은 글 도메인.
- **Brand voice 자동 추출** (v1.x) — 사용자 글 샘플 → brand voice frontmatter 생성 도구 (별도 script).
- **LLM-as-judge eval** (v1.x) — 정성 자연스러움 / 의미 보존 자동 평가 metric (M6+).
- **Batch / API mode** (v1.x) — 다수 텍스트 일괄 humanize 인터페이스.
- **사용자 만족도 정량 측정** (별도 트랙) — A/B test, NPS 등.

위 후보들은 freeze 영역을 깨지 않는다 — 모두 1.x.0 minor 로 진행 가능.

다음 major (2.0) 가 필요한 시점은:

- 실 사용 데이터로 **카테고리 #13** 군이 발견될 때 (현 12 카테고리로 못 잡는 새 AI 티 패턴군).
- 정량 룰 cap 의 데이터 기반 재교정 결과 freeze 값이 부적절할 때.

이런 경우 v1.x 막바지에 v2 RFC → community 협의 → v2 major bump.

---

## 참고

- [CHANGELOG](../CHANGELOG.md) — 모든 버전 history
- [Migration 0.x → 1.0](MIGRATION-0.x-to-1.0.md) — v1.0 진입 시 변경 사항
- [Security Policy](../SECURITY.md) — 보안 이슈 보고
- [Roadmap](../ROADMAP.md) — sprint 단위 계획
