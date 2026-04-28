# korean-humanizer

> 한국어로 쓰인 AI 생성 텍스트에서 "AI 티"를 걷어내 자연스럽게 다듬는 작은 skill / system prompt.
>
> *A tiny skill that strips "AI smell" from Korean text — works in Claude Code, Claude.ai, ChatGPT, Cursor, Gemini, and any LLM.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-100%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Korean](https://img.shields.io/badge/lang-Korean-red.svg)](#)

---

## 왜 만들었나

영어용 humanizer skill (`blader/humanizer`, `jalaalrd/anti-ai-slop-writing` 등)은 많지만, **한국어 전용 humanizer는 비어 있었다.** 한국어에는 영어와 다른 AI tell이 있다 — 번역체("~에 있어서"), 격식체 남용("~인 것이다"), "이러한 / 해당" 과다, AI 고빈도 어휘("활용 / 극대화 / 시사한다") 같은 것들.

이 레포는 그 빈자리를 채우는 **100여 개의 한국어 AI 패턴 카탈로그**와, 그걸 적용하는 작은 skill / 시스템 프롬프트를 묶었다.

---

## 5분 안에 시작하기

### ① Claude Code / Cowork

```bash
git clone https://github.com/dotoricode/korean-humanizer ~/.claude/skills/korean-humanizer
```

새 세션에서 "한국어 humanizer로 다듬어줘" 또는 "AI 티 빼줘" 라고 하면 활성화된다.

### ② Claude.ai

[`SKILL.md`](SKILL.md) 와 [`references/ko-ai-signals.md`](references/ko-ai-signals.md) 를 다운로드해 프로젝트 / 대화에 업로드.

### ③ ChatGPT / Cursor / Gemini / 기타 LLM

[`PROMPT.md`](PROMPT.md) 전체를 시스템 프롬프트(또는 첫 메시지)에 붙여 넣고 한국어 텍스트를 입력하면 된다.

---

## 패턴 미리보기

12 카테고리 / 100+ 패턴 중 강한 것 몇 개:

| 카테고리 | 나쁨 | 자연스러움 |
|---|---|---|
| 강조어 남발 | 매우 중요한 | 중요한 / 꽤 중요한 |
| 공허한 형용사 | 다양한 방법 | 몇 가지 방법 |
| 번역체 | ~에 있어서 / ~함에 있어 | ~에서 / ~할 때 |
| "것이다" 과다 | 사실 ~인 것이다 | 사실 ~예요 / ~다 |
| "이러한 / 해당" | 해당 시스템은 | 그 시스템은 |
| 판에 박힌 개시 | 안녕하세요! 오늘은~ 알아보겠습니다 | (바로 본론) |
| 수동태 | 고려되어야 합니다 | 고려해야 한다 |
| 연결어 남발 | 또한 / 따라서 / 결론적으로 | (대부분 삭제) |
| AI 고빈도 어휘 | 활용 / 극대화 / 시사한다 | 사용 / 가장 크게 / 보여준다 |

전체 카탈로그 → [`references/ko-ai-signals.md`](references/ko-ai-signals.md)

---

## 변환 사례

**Before** *(AI 원문)*

> 안녕하세요! 오늘은 매우 중요한 주제인 시간 관리에 대해 알아보겠습니다. 다양한 사람들이 시간 관리에 어려움을 겪고 있는데요, 본 글에서는 효과적인 시간 관리 방법을 체계적으로 살펴보도록 하겠습니다.

**After** *(humanized)*

> 시간 관리 얘기를 해보려고 한다. 시간 관리 안 되는 사람이 많다. 이 글에서 쓸 만한 방법 몇 개를 정리한다.

→ 패턴 카탈로그 적용 예시: [`examples/before-after.md`](examples/before-after.md)
→ **실제 에이전트 raw 출력 vs skill 적용 비교** (4 도메인 / 정량·정성 분석): [`examples/agent-vs-skill.md`](examples/agent-vs-skill.md)

---

## 핵심 룰 (왜 이걸 따르는가)

humanizer는 다음 4가지 안전장치를 지킨다:

1. **의미 불변** — 팩트 / 숫자 / 고유명사 / 인용문 / 링크는 절대 바꾸지 않는다.
2. **20% cap** — 전체 텍스트의 20% 이상 수정하지 않는다 (긴 글일수록 가볍게 터치).
3. **문단 3곳 룰** — 한 문단에 3곳 이상 건드리지 않는다.
4. **자연스러움 > 완벽함** — 살짝 덜 매끄러운 게 더 사람답다. 과도한 세련미는 오히려 AI 티.

---

## 커스터마이징

자주 쓰는 금지어 / 선호어가 있다면 [`examples/personal-list.md`](examples/personal-list.md) 템플릿을 편집해서 사용. personal list는 카탈로그보다 **먼저** 적용된다.

```yaml
금지: ["활용", "매우", "다양한"]
선호:
  - "유용하다" → "쓸만하다"
유지: ["결과적으로"]  # 의도적으로 쓰는 단어
```

---

## 파일 구조

```
korean-humanizer/
├── README.md                  # 이 파일
├── SKILL.md                   # Claude Code / Cowork 진입점
├── PROMPT.md                  # 일반 LLM 시스템 프롬프트
├── LICENSE                    # MIT
├── references/
│   └── ko-ai-signals.md       # 100+ 패턴 카탈로그 (메인 IP)
└── examples/
    ├── before-after.md        # 패턴 카탈로그 적용 사례 (3 도메인)
    ├── agent-vs-skill.md      # 실제 에이전트 raw vs skill 적용 비교 (4 도메인)
    └── personal-list.md       # 사용자 커스터마이징 템플릿
```

---

## 적용하지 않는 경우

- 영어 / 일본어 / 중국어 등 한국어가 아닌 텍스트
- 코드, 코드 주석, 기술 문서 (정확성 우선)
- 법률 / 규제 / 공식 문서 (격식이 의도된 것)
- 단순 오탈자 / 문법 교정 (proofreading 도구가 적절)
- 사용자가 "원문 그대로" 요청한 경우

---

## Contribution

패턴 추가 PR / Issue 환영. 새 카테고리를 제안하거나, 기존 카테고리에 표 row를 추가하거나, 다른 도메인의 변환 사례를 보내주면 좋다.

좋은 PR의 특징:
- 패턴 1~5개를 같은 카테고리 안에 모아 추가
- "왜 AI 티인지" 짧은 한 줄 설명
- 가능하면 before/after 예시 한 쌍

---

## License

MIT — 마음대로 사용, 수정, 배포, 상업 이용 가능. 표기 의무 외엔 제한 없음.

---

*Authored by [dotoricode](https://github.com/dotoricode) · MIT License*
# korean-humanizer
