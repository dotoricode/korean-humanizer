# Contributing to korean-humanizer

> 한국어 AI 글쓰기 패턴 카탈로그 + skill / system prompt. PR / Issue 모두 환영합니다.

## 어떤 기여가 가능한가요?

| 종류 | 어디로 | 예시 |
|---|---|---|
| 새 패턴 추가 | `references/ko-ai-signals.md` | "~을 야기합니다" → "~을 일으킨다" 같은 한 줄 추가 |
| 새 카테고리 제안 | Issue → 합의 후 PR | 12 카테고리 외에 새로 발견한 패턴 묶음 |
| 새 도메인 비교 사례 | `examples/agent-vs-skill.md` | 게임 리뷰 / 학술 논문 인트로 / 정부 보도자료 등 |
| 패턴 카탈로그 적용 예시 | `examples/before-after.md` | 새 도메인의 before/after 한 쌍 |
| 룰 / 출력 포맷 제안 | Issue 먼저 (큰 변경) | `SKILL.md` / `PROMPT.md` 수정안 |
| 오타·문장 다듬기 | PR 직접 | 작은 개선은 issue 없이 PR OK |

## 작업 전에 알아둘 것 (3가지)

### 1. 카탈로그가 single source of truth

`references/ko-ai-signals.md` 의 12 카테고리 라벨이 모든 examples / SKILL / PROMPT의 source. examples에서 카테고리 라벨을 인용할 때는 카탈로그와 1:1로 맞아야 합니다(과거에 "보다"를 번역체로, "선사"를 AI 고빈도로 잘못 라벨한 사례 있음 — 카탈로그에 없는 라벨은 새 패턴 PR로 먼저 추가).

### 2. 정량 한도는 SKILL ↔ PROMPT ↔ 카탈로그 3곳에서 일치

"한 문단 3곳" / "전체 문장 수의 20%" 룰은 세 파일에 같은 표현으로 들어 있습니다. 한 곳만 바꾸면 drift가 생깁니다 — 룰 변경 PR은 세 파일 동시에 수정해야 합니다.

### 3. 의미 불변이 최우선

humanizer는 "표현"만 바꾸고 의미는 절대 바꾸지 않습니다. 새 패턴 추가 시 우측 "자연스러움" 컬럼이 좌측 "나쁨"의 의미를 바꾸지 않는지 확인하세요.

### 4. 빈도 컬럼 분류 기준

`references/ko-ai-signals.md` 의 표준 패턴 표 (`| 나쁨 | 자연스러움 | 빈도 | 적용 도메인 |`) 는 빈도 컬럼이 필수입니다. 새 패턴을 추가할 때 다음 기준으로 한 값을 부여하세요.

| 빈도 | 기준 |
|---|---|
| **high** | KatFish / XDAC 등 한국어 탐지 연구에서 빈출로 보고됐거나, 일상적인 LLM 한국어 출력에서 한 글에 1 회 이상 나타나는 패턴. 우선 다듬을 가치가 가장 큼. |
| **med** | 도메인 일부 (마케팅·뉴스레터·격식 글) 에서 자주 보이지만, 글 전반에 빈출하지는 않는 패턴. 디폴트 값. |
| **low** | 드물지만 명확한 AI signal — 특정 모델 / 특정 프롬프트에서 가끔 출현. 현재 카탈로그에는 거의 없음. 의심스러우면 `med` 로 두는 게 안전. |

기여자가 빈도를 자신할 수 없으면 **med** 를 기본값으로 두면 됩니다. 데이터 기반 재라벨링은 raw 샘플 수집 후 별도 1.x 유지보수 트랙에서 검토합니다 (`eval/frequency-data/README.md` 참고).

### 5. 적용 도메인 컬럼 분류 기준 *(v0.8 카탈로그 v2)*

표준 패턴 표의 4 번째 컬럼 `적용 도메인` — 패턴이 강하게 작동하는 도메인을 명시합니다. 부록 F 의 valid 도메인 코드를 사용하세요.

| 값 형식 | 사용 시점 | 예시 |
|---|---|---|
| `all` | 12 도메인 모두에서 강하게 작동하는 보편 AI 티 | "사실 ~인 것이다", "또한 ~할 수 있습니다", 강조어 일반 |
| `marketing,review` | 2-3 도메인에 치우친 패턴 | "혁신적인 솔루션", "안전하고 빠르고 저렴하다" |
| `formal` (= `email,b2b-message,academic`) | shorthand 가 정확히 맞는 격식 도메인 패턴 | "다음과 같습니다", "고려되어야 합니다" |
| `academic,wiki` | 학술 / 문서체 빈출 | "활용되어 왔다", "여러 가지 측면에서" |

**판단 룰**:

- **잘 모르겠으면 `all`**: v0.7 호환 = 안전 디폴트.
- **shorthand (`all` / `informal` / `formal`) 는 정확히 맞을 때만**: 부분 셋이면 콤마 표기.
- **`all` 단독 사용 의무**: `all` 과 다른 코드 혼용 금지 (`all,marketing` X, `marketing,review` O).

도메인 코드 표준 전체 → [`references/ko-ai-signals.md` 부록 F](references/ko-ai-signals.md#부록-f-도메인-코드-표준).

### 6. Brand voice 사례 PR *(v0.8)*

`examples/brand-voice-<name>.md` 케이스 스터디 추가 시:

- **가상 케이스만 받습니다** — 실재 기업 / 작가의 brand voice 모방은 받지 않음 (공정 경쟁 / 저작 인격권 보호).
- 템플릿 (`examples/brand-voice-template.md`) 의 frontmatter + 톤 가이드 + 라이브 예시 (raw → humanized) 형식 그대로.
- preserve / ban / prefer 가 의미 있게 작동하는 raw → humanized 사례 2-3 개 권장.
- 이미 있는 두 케이스 (Toss 풍 / 작가 X) 와 **의도적으로 다른 끝점** 인 brand voice 가 좋은 후보 (예: 학술 풍 / 게임 캐주얼 / 청년층 SNS 톤 등).

## PR 체크리스트

PR을 올리기 전에 아래를 확인해주세요:

- [ ] 새 패턴은 카탈로그의 12 카테고리 중 하나에 들어가는가? (아니면 Issue로 새 카테고리 제안 먼저)
- [ ] "나쁨" → "자연스러움" 매핑이 의미를 바꾸지 않는가?
- [ ] **표준 패턴 표 (나쁨 | 자연스러움 | 빈도 | 적용 도메인) 의 4 컬럼을 모두 채웠는가?** (기준은 위 §4 / §5)
- [ ] **적용 도메인 값이 valid 도메인 코드인가?** (`all` / `informal` / `formal` / 12 개별 도메인 콤마 리스트, `all` 은 단독)
- [ ] examples에서 카테고리 라벨을 사용한다면, 카탈로그와 1:1 매칭되는가?
- [ ] 정량 수치(자수, 압축률 등)에는 추정치 단서(±오차)가 있는가?
- [ ] CTR / 시간 정밀 같은 데이터 없는 주장이 들어가지 않았는가? (구조적 사실로만)
- [ ] 새 도메인 비교 사례라면, raw 출력은 humanizer 룰을 의식하지 않고 평소대로 생성된 것인가?
- [ ] **로컬 lint / eval 통과 (4 종)**:
  - [ ] `bash scripts/lint-patterns.sh` ✓ — 카탈로그 표 형식 + 빈도 + 적용 도메인 컬럼 + 도메인 코드 valid (v2)
  - [ ] `bash scripts/lint-cross-file.sh` ✓ — SKILL/PROMPT/카탈로그 정량 규칙·카테고리·brand voice (4 번째 mode)·부록 F sync
  - [ ] `bash scripts/lint-examples.sh` ✓ — 예시 "주요 변경 (최대 5개)" 룰 + 카테고리 범위
  - [ ] `bash scripts/eval-harness.sh` ✓ — fixture 5 metric (M1 수정비율 / M2 단락cap / M3 길이 / M4 ~다체 / M5 brand preserve — M5 는 옵션)
  - [ ] markdownlint warning 은 무시해도 OK
- [ ] 새 fixture 를 더할 때 — `eval/fixtures/<domain>-NN-<name>.md` 형식 + frontmatter 채움. brand voice 사례는 `brand_voice: examples/brand-voice-<name>.md` 추가. 가이드: [`eval/README.md`](eval/README.md)
- [ ] **새 도메인 사례 (`examples/domain-*.md`)**: 메타데이터 (도메인 / 강한 카테고리 / 톤 디폴트 / 톤 보존 / 금지 변경) + Raw + Humanized + 변경 (≤ 5) + 보존 + 개선 포인트 + 한계 + 도메인 적용 가이드 모두 채움. `references/ko-ai-signals.md` 부록 E 의 도메인 우선순위 표에도 row 추가, 부록 F 도메인 코드 표에도 행 추가, lint-patterns.sh 의 valid 도메인 셋 갱신.
- [ ] **Brand voice 케이스 스터디 (`examples/brand-voice-*.md`)**: §6 의 가이드 따름. 가상 케이스만, frontmatter 7 필드 + 톤 가이드 + raw → humanized 2-3 사례.

## 좋은 PR의 특징

- **작게.** 카탈로그에 1~5개 패턴 추가. 한 카테고리에 모아서.
- **출처 한 줄.** "왜 이게 AI 티인지" 짧은 설명(번역체 출처? 모델 출력 관찰?).
- **before/after 1쌍.** 가능하면 examples/before-after.md에 한 쌍 함께 추가.
- **도메인 명시.** 어떤 글에서 발견했는지(블로그·이메일·LinkedIn 등) 짧게.

## 좋은 Issue의 특징

- **재현 가능.** "이 프롬프트로 모델이 자주 출력함" 같이 구체적으로.
- **카테고리 후보.** 새 카테고리 제안이면, 12 카테고리 중 어디에도 안 맞는 이유.
- **샘플 1~2개.** raw 출력을 그대로 박아주기.

## 라이선스

이 프로젝트는 [MIT License](LICENSE) 입니다. PR을 보내면 MIT 하에 기여한 것으로 간주합니다.

## 행동 강령

- 한국어 / 영어 OK.
- 모든 패턴 제안은 "AI 티"라는 객관적 관찰에 한정합니다 — 특정 화자나 채널을 비하하는 패턴은 받지 않습니다.
- 정치·종교·인종 관련 표현 패턴은 별도 정책 협의가 필요합니다(현재 정책: 패턴 자체가 차별·비하 의도라면 거부).

질문은 [Issues](https://github.com/dotoricode/korean-humanizer/issues)에서.
