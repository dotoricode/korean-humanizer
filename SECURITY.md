# Security Policy

> `korean-humanizer` 는 humanize **편집 보조** skill 이며 사용자 입력을 외부로 송신하지 않는다 (LLM 호출은 호스트 환경 — Claude / GPT / Gemini — 의 책임). 그래도 다음 영역에서 보안 / 안전 이슈가 발생할 수 있으니 절차를 명문화한다.

---

## 지원 버전

| 버전 | 지원 상태 |
|---|---|
| 1.x | ✓ 보안 패치 지원 (~12 개월) |
| 0.8.x | ✓ critical 한정 (v1.0 출시 후 3 개월) |
| 0.7.x 이하 | ✗ 지원 종료 — v1.0 으로 업그레이드 권장 |

---

## 보고 방법

### 비공개 보고 (권장)

다음 중 한 채널로:

1. **GitHub Security Advisory** — 이 레포의 `Security` 탭 → `Report a vulnerability` (가장 권장).
2. **Email** — 메인테이너 (dotori, GitHub: [@dotoricode](https://github.com/dotoricode)) 의 commit author email 로 직접 보내기. (스팸 방지 위해 평문 표기 안 함.)

**제목 prefix**: `[security]` 권장 — triage 가속.

### 공개 issue 로 올리지 마세요

비공개 보고가 어려우면 임시로 issue 에 "민감한 이슈 — 비공개로 연락 부탁" 한 줄만 남기고, 메인테이너가 비공개 채널을 안내합니다. 디테일은 issue 본문에 절대 쓰지 마세요 (의존 사용자 보호 차원).

---

## 응답 시간

| 단계 | 목표 시간 |
|---|---|
| 수신 confirm | 24 시간 |
| 초기 triage (severity 평가) | 72 시간 |
| 수정 일정 공유 | 7 일 |
| Critical 패치 release | severity 에 따라 — 보고자와 합의 |

---

## 범위 (in-scope)

### 1. Skill 코드 / CI / scripts

- `scripts/eval-harness.py`, `scripts/lint-*.sh`, `.github/workflows/*` 의 의도하지 않은 동작 (예: 사용자 환경에서 임의 명령어 실행, 외부 통신).
- CI workflow 의 secret leak / 권한 escalation.

### 2. 카탈로그 / 룰의 의도되지 않은 의미 변경

humanizer 의 핵심 약속은 **의미 불변**. 다음은 의미 변경 → 보안 / 안전 이슈로 분류:

- 카탈로그 패턴이 **숫자 / 고유명사 / 인용문 / 링크 / 의학·법률·재무 정보** 를 변경하도록 유도하는 경우.
- Brand voice / personal list 입력이 **의미 보존 룰을 우회** 시키는 vector (예: 특정 단어 매핑이 fact 를 바꿈).
- 도메인 디폴트가 **법률·의료·금융 도메인의 격식 강제 룰** 을 깨뜨리는 경우.

### 3. 사용자 입력 처리에서 PII / 비밀 노출

- 카탈로그 / examples / fixture 에 의도치 않게 들어간 PII / API key / 내부 도메인.
- Brand voice / personal list 파일이 sensitive 정보 (개인 톤이 곧 신원 식별) 를 그대로 git commit 되도록 유도하는 워크플로우 결함.

### 4. Supply chain

- npm / PyPI / homebrew dependency 가 추가되는 PR — `korean-humanizer` 는 **stdlib 만 사용** 정책. 새 의존 추가 PR 은 보안 검토 의무.
- GitHub Action 의 third-party action 사용 — pinned SHA 의무.

---

## 범위 외 (out-of-scope)

- **호스트 LLM 의 보안** (Claude / GPT / Gemini API 자체) — vendor 에 보고.
- **사용자가 humanize 한 텍스트의 fact-checking** — humanizer 는 표현만 다듬음. fact-checker 는 별도 도구 (`fact-checker` skill).
- **AI 탐지 우회 / 회피 의도의 사용** — humanizer 는 의미 보존 자연화이지 detector 회피가 아님. detector 회피 목적의 PR / Issue 는 거부.
- **다국어 확장** (영구 out-of-scope, 한국어 전용).

---

## Severity 분류

| 등급 | 정의 | 예시 | 응답 |
|---|---|---|---|
| **Critical** | 의미 불변 깨짐 + 광범위 영향 | 숫자 / 고유명사 자동 변경 패턴이 카탈로그에 추가됨 | 24 시간 내 hot-fix |
| **High** | PII 노출 / supply chain | 외부 API 호출 코드 추가 PR | 7 일 내 |
| **Medium** | 의도되지 않은 동작 | lint 가 false positive 로 valid 표를 reject | 14 일 내 |
| **Low** | 안전성 미흡 | 문서에 보안 가이드 누락 | next minor |

---

## 책임 공개 (Responsible Disclosure)

- 비공개 보고 → 패치 → release → **공개 disclosure** 순서.
- 보고자 credit 은 보고자 동의 시 release notes / SECURITY.md 에 표기.
- Critical 이슈는 patch release 시 GitHub Security Advisory 동시 공개.

---

## 개인 정보 / PII 가이드 (사용자 측)

`korean-humanizer` 는 **사용자 입력을 어디에도 송신하지 않습니다** (호스트 LLM 통신은 Claude / GPT / Gemini 의 책임). 그래도 다음을 권장:

- humanize 입력에 실명 / 이메일 / 전화번호 / 계좌번호 / API key 같은 sensitive 정보가 있으면 **익명화 후** 입력.
- Brand voice 파일을 public repo 에 commit 하기 전 — `preserve` / `ban` 단어가 식별 가능한 사내 / 개인 정보를 노출하지 않는지 점검.
- Issue 에 raw / humanized 텍스트를 붙일 때 — PII 마스킹 후.

---

## 참고

- [Stability Promise](docs/STABILITY-PROMISE.md) — v1.0 freeze 영역
- [Migration guide](docs/MIGRATION-0.x-to-1.0.md) — 보안 영향 있는 변경 사항
- [Contributing](CONTRIBUTING.md) — PR 보안 체크리스트
