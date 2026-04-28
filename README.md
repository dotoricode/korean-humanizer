# korean-humanizer

> 한국어로 쓰인 AI 생성 텍스트에서 "AI 티"를 걷어내 자연스럽게 다듬는 작은 skill / system prompt.
>
> *A tiny skill that strips "AI smell" from Korean text — works in Claude Code, Claude.ai (Cowork), ChatGPT, Cursor, Gemini, and any LLM.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-100%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Korean](https://img.shields.io/badge/lang-Korean-red.svg)](#)

## Installation

### Claude Code

Claude Code 의 skills 디렉토리에 그대로 clone 한다.

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

이미 레포가 로컬에 있으면 skill 파일만 복사해도 된다.

```bash
mkdir -p ~/.claude/skills/korean-humanizer
cp SKILL.md ~/.claude/skills/korean-humanizer/
cp -r references ~/.claude/skills/korean-humanizer/
```

### Claude.ai (Cowork) / Project

[`SKILL.md`](SKILL.md) 와 [`references/ko-ai-signals.md`](references/ko-ai-signals.md) 를 다운로드해 프로젝트나 대화에 업로드한다.

### ChatGPT / Cursor / Gemini / 기타 LLM

[`PROMPT.md`](PROMPT.md) 전체를 시스템 프롬프트(또는 첫 메시지)에 붙여 넣고 다듬을 한국어 텍스트를 입력하면 된다.

## Usage

### Claude Code

```
/korean-humanizer

[다듬을 한국어 텍스트 붙여넣기]
```

또는 자연어로 요청해도 활성화된다.

```
이거 AI 티 빼줘:
[텍스트]
```

```
한국어 humanizer 로 자연스럽게 다듬어줘:
[텍스트]
```

### Claude.ai / ChatGPT / Cursor / Gemini

`PROMPT.md` 를 시스템 프롬프트에 붙여 넣은 뒤 한국어 텍스트만 입력하면 된다. 별도 명령어 없이 바로 humanize 된다.

### Personal List 캘리브레이션

자기 톤에 맞추려면 자주 쓰는 금지어 / 선호어 / 유지어를 [`examples/personal-list.md`](examples/personal-list.md) 템플릿에 적어 함께 제공한다. personal list 는 카탈로그 패턴보다 **먼저** 적용된다.

```yaml
금지: ["활용", "매우", "다양한"]
선호:
  - "유용하다" → "쓸만하다"
유지: ["결과적으로"]   # 의도적으로 쓰는 단어는 humanizer 가 건드리지 않는다
```

```
/korean-humanizer

내 personal list:
[paste personal-list.md content]

이 텍스트 다듬어줘:
[paste AI text]
```

## Overview

영어용 humanizer skill (`blader/humanizer`, `jalaalrd/anti-ai-slop-writing` 등)은 많지만, **한국어 전용 humanizer 는 비어 있었다.** 한국어에는 영어와 다른 AI tell 이 있다 — 번역체("~에 있어서"), 격식체 남용("~인 것이다"), "이러한 / 해당" 과다, AI 고빈도 어휘("활용 / 극대화 / 시사한다") 같은 것들.

이 레포는 그 빈자리를 채우는 **12 카테고리 / 100+ 한국어 AI 패턴 카탈로그**와 그걸 적용하는 작은 skill / 시스템 프롬프트를 묶었다.

### 핵심 원칙

> "AI 가 쓴 한국어는 읽으면 티가 난다. humanizer 는 그 티를 걷어낸다 — **의미는 그대로 두고 표현만**."

humanizer 는 다음 4 가지 안전장치를 지킨다:

1. **의미 불변** — 팩트 / 숫자 / 고유명사 / 인용문 / 링크는 절대 바꾸지 않는다.
2. **20% cap** — 전체 문장 수의 20% 이상 수정하지 않는다 (긴 글일수록 가볍게 터치).
3. **문단 3곳 룰** — 한 문단에 3곳 이상 건드리지 않는다.
4. **자연스러움 > 완벽함** — 살짝 덜 매끄러운 게 더 사람답다. 과도한 세련미는 오히려 AI 티.

## 12 Categories Detected (with Before/After Examples)

각 카테고리는 9~14 개 세부 패턴 표로 펼쳐져 있다. 전체 카탈로그 → [`references/ko-ai-signals.md`](references/ko-ai-signals.md)

### Content Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **강조어 남발** (Empty Intensifiers) | "**매우** 중요한 / **굉장히** 획기적인" | "중요한 / 새로운" |
| 2 | **공허한 형용사** (Empty Adjectives) | "**다양한** 방법 / **혁신적인** 솔루션 / **포괄적인** 가이드" | "세 가지 방법 / 새 방식 / 처음부터 끝까지" |

### Language Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 3 | **번역체 / 과격식** (Translation-ese) | "~에 있어서 / ~을 통해 / ~에 의해 / ~함에 있어" | "~에서 / ~로 / ~가 / ~할 때" |
| 4 | **"것이다 / 이러한 / 해당" 과다** | "사실 ~인 것이다 / 이러한 이유로 / 해당 시스템은" | "사실 ~다 / 이 때문에 / 그 시스템은" |
| 6 | **수동태 / 모호한 주어** | "고려되어야 합니다 / 활용되어 왔다 / 평가되고 있다" | "고려해야 한다 / 자주 쓰였다 / (누가) 평가한다" |
| 7 | **불필요한 연결어** (Filler Connectives) | "또한 / 뿐만 아니라 / 따라서 / 결론적으로" | (대부분 삭제. 새 문장으로 시작) |
| 12 | **AI 고빈도 어휘** (Korean LLM Tells) | "활용 / 극대화 / 시사한다 / 도모 / 모색 / ~의 일환으로" | "사용 / 가장 크게 / 보여준다 / 챙기기 / 찾기 / (삭제)" |

### Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 5 | **판에 박힌 개시 / 마무리** | "안녕하세요! 오늘은 ~에 대해 알아보겠습니다 ... 도움이 되셨길 바랍니다!" | (바로 본론, 그냥 끝) |
| 8 | **과도한 3항 나열** (Forced Triplets) | "빠르고 정확하며 효율적입니다. 간단하고 명확하며 실용적입니다." | "빠르고 정확하다. 쓰기도 어렵지 않다." |
| 10 | **이모지 / 이모티콘 남발** | "🚀 **시작하기** 💡 **핵심 포인트** ✨ **결론** 👏" | (헤더당 0~1 개. 의미 있는 자리에만) |

### Communication Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 9 | **존댓말 레벨 불일치** | "안녕하세요~ 반가워요! ... 가능하시다면 ~하시기 바랍니다." | (전체 톤 통일. "해요체"면 끝까지 "해요체") |

### Filler and Hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 11 | **단정 회피 / 과한 hedging** | "~라고 할 수 있습니다 / 아마도 ~인 것 같습니다 / 어느 정도는" | "~다 / ~예요 (단언)" |

## Full Example

**Before** *(AI 원문)*

> 안녕하세요! 오늘은 매우 중요한 주제인 시간 관리에 대해 알아보겠습니다. 다양한 사람들이 시간 관리에 어려움을 겪고 있는데요, 본 글에서는 효과적인 시간 관리 방법을 체계적으로 살펴보도록 하겠습니다.
>
> 시간 관리는 단순히 일정을 정리하는 것을 넘어, 우리의 삶의 질을 결정하는 핵심 요소라고 할 수 있습니다. 또한 업무 효율성을 극대화하고, 일과 삶의 균형을 보다 효과적으로 유지하는 데 있어서 매우 중요한 역할을 한다고 평가되고 있습니다. 따라서 이러한 시간 관리 능력은 현대인에게 필수적인 역량이라고 할 수 있는 것입니다.
>
> 본 글에서는 다음과 같은 핵심 전략을 다룰 예정입니다:
>
> - 🚀 **우선순위 설정**: 중요한 일과 급한 일을 구분하는 방법
> - 💡 **시간 블록킹**: 시간을 효과적으로 분할하여 활용하는 기법
> - ✨ **방해 요소 제거**: 집중력을 극대화하는 환경 조성 방법
>
> 도움이 되셨길 바라며, 궁금한 점이 있으시면 언제든지 댓글로 남겨주세요. 함께 더 나은 시간 관리 습관을 만들어 가봅시다! 감사합니다 🙌

**After** *(humanized)*

> 시간 관리 얘기를 해보려고 한다. 시간 관리가 안 되는 사람은 많고, 이 글에서 쓸 만한 방법 몇 개를 정리한다.
>
> 시간 관리는 일정 정리에 그치지 않는다. 삶의 질을 가르는 부분이고, 업무 효율과 일·삶 균형에도 큰 영향을 준다. 그래서 현대인에게 필요한 능력이다.
>
> 이 글에서 다룰 핵심은 셋이다.
>
> - **우선순위 설정**: 중요한 일과 급한 일을 가르는 방법
> - **시간 블록킹**: 시간을 잘라 쓰는 기법
> - **방해 요소 제거**: 집중하기 좋은 환경 만들기

→ 패턴 카탈로그 적용 사례: [`examples/before-after.md`](examples/before-after.md)
→ **실제 에이전트 raw 출력 vs skill 적용 비교** (6 도메인 / 정량·정성 분석): [`examples/agent-vs-skill.md`](examples/agent-vs-skill.md)

## When Not to Apply

- 영어 / 일본어 / 중국어 등 한국어가 아닌 텍스트
- 코드, 코드 주석, 기술 문서 (정확성 우선)
- 법률 / 규제 / 공식 문서 (격식이 의도된 것)
- 단순 오탈자 / 문법 교정 (proofreading 도구가 적절)
- 사용자가 "원문 그대로" 요청한 경우

## File Structure

```
korean-humanizer/
├── README.md                  # 이 파일
├── SKILL.md                   # Claude Code / Cowork 진입점
├── PROMPT.md                  # 일반 LLM 시스템 프롬프트
├── LICENSE                    # MIT
├── CONTRIBUTING.md            # 기여 가이드
├── .github/ISSUE_TEMPLATE/    # 패턴 추가 / 도메인 사례 / 버그 보고 템플릿
├── references/
│   └── ko-ai-signals.md       # 12 카테고리 / 100+ 패턴 카탈로그 (메인 IP)
└── examples/
    ├── before-after.md        # 패턴 카탈로그 적용 사례 (3 도메인)
    ├── agent-vs-skill.md      # 실제 에이전트 raw vs skill 적용 비교 (6 도메인)
    └── personal-list.md       # 사용자 커스터마이징 템플릿
```

## References

- [`references/ko-ai-signals.md`](references/ko-ai-signals.md) — 12 카테고리 / 100+ 한국어 AI 패턴 카탈로그 (메인 IP)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — 영어 패턴 1차 소스 (영감)
- [`blader/humanizer`](https://github.com/blader/humanizer) — 영어 humanizer skill (구조 참고)
- [`jalaalrd/anti-ai-slop-writing`](https://github.com/jalaalrd/anti-ai-slop-writing) — 영어 anti-slop 가이드

## Contribution

패턴 추가 PR / Issue 환영. 새 카테고리를 제안하거나, 기존 카테고리에 표 row 를 추가하거나, 다른 도메인의 변환 사례를 보내주면 좋다.

상세 가이드와 PR 체크리스트는 [`CONTRIBUTING.md`](CONTRIBUTING.md) 참고.

Issue 템플릿: [패턴 추가](.github/ISSUE_TEMPLATE/pattern_addition.md) / [새 도메인 사례](.github/ISSUE_TEMPLATE/new_domain_case.md) / [버그 보고](.github/ISSUE_TEMPLATE/bug_report.md).

좋은 PR 의 특징:
- 패턴 1~5 개를 같은 카테고리 안에 모아 추가
- "왜 AI 티인지" 짧은 한 줄 설명
- 가능하면 before / after 예시 한 쌍

## Version History

- **0.2.0** — 에이전트 raw 출력 vs skill 적용 비교 자료 추가 (`examples/agent-vs-skill.md`, 6 도메인 정량·정성 비교)
- **0.1.0** — 초기 공개. 12 카테고리 / 100+ 패턴 카탈로그, SKILL.md, PROMPT.md, before-after / personal-list 예제

## License

MIT — 마음대로 사용, 수정, 배포, 상업 이용 가능. 표기 의무 외엔 제한 없음.

---

*Authored by [dotoricode](https://github.com/dotoricode) · MIT License*
