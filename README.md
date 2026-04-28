# korean-humanizer

> 한국어로 쓰인 AI 생성 텍스트에서 "AI 티"를 걷어내 자연스럽게 다듬는 작은 skill / system prompt.
>
> *A tiny skill that strips "AI smell" from Korean text — works in Claude Code, Claude.ai (Cowork), OpenCode, Codex, ChatGPT, Cursor, Gemini, and any LLM.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-100%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Korean](https://img.shields.io/badge/lang-Korean-red.svg)](#)
[![Wiki](https://img.shields.io/badge/wiki-research-purple.svg)](https://github.com/dotoricode/korean-humanizer/wiki)

<!-- 데모 GIF: 사용자가 assets/demo.gif 를 푸시한 뒤 아래 줄의 주석을 해제하세요. 녹화 가이드 → assets/RECORDING.md -->
<!-- ![korean-humanizer 데모: raw → humanized 변환 (30초)](assets/demo.gif) -->

## What it does — 5초 요약

| Before *(AI 원문)* | After *(humanized)* |
|---|---|
| 🚀 **혁신적인** 솔루션을 **활용하여** **다양한** 비즈니스 **가치를 극대화**하고, **이러한 접근을 통해** 사용자 경험을 **한층 더** **고도화**할 수 있습니다. ✨ | 이 방식으로 비즈니스 가치를 키우고, 사용자 경험도 더 좋게 만들 수 있어요. |
| 지난 6개월간 **다양한** 프로젝트를 **통해** **많은 것을 배우고 성장할 수 있었던** **의미 있는** 시간이었습니다. **이러한** 경험은 앞으로의 커리어에 **있어서** **매우 소중한** 자산이 될 것이라고 **확신합니다**. 🙌 | 지난 6개월 동안 프로젝트 몇 개 하면서 많이 배웠어요. 다음에 또 써먹을 경험이라 좋았어요. |
| 본 사항은 **다양한** 측면에서 **신중하게 고려되어야** 할 필요가 있을 것으로 **사료됩니다**. | 이 건은 좀 더 봐야 할 것 같아요. |

**한국어 LLM 출력의 12 카테고리 / 100+ AI 티 패턴**을 의미 불변으로 다듬는다 (Claude Code · Claude.ai · OpenCode · Codex · Cursor · ChatGPT · Gemini 호환).

🔗 [Wiki (연구 / 평가 / 윤리)](https://github.com/dotoricode/korean-humanizer/wiki) · 🛠️ [패턴 카탈로그 (메인 IP)](references/ko-ai-signals.md) · 💬 [Issues](https://github.com/dotoricode/korean-humanizer/issues/new/choose) · 📑 [전체 비교 사례](#full-example)

## Overview

영어용 humanizer skill (`blader/humanizer`, `jalaalrd/anti-ai-slop-writing` 등)은 많지만, **한국어 전용 humanizer 는 비어 있었다.** 한국어에는 영어와 다른 AI tell 이 있다 — 번역체("~에 있어서"), 격식체 남용("~인 것이다"), "이러한 / 해당" 과다, AI 고빈도 어휘("활용 / 극대화 / 시사한다") 같은 것들. 최근 한국어 탐지 연구(KatFish, XDAC) 도 쉼표 과다 / 명사 편중 / 종결어미 단조로움 / 낮은 어휘 다양성을 한국어 전용 신호로 짚는다.

이 레포는 그 빈자리를 채우는 **12 카테고리 / 100+ 한국어 AI 패턴 카탈로그**와 그걸 적용하는 작은 skill / system prompt 를 묶었다. 연구 근거와 평가 루브릭은 [`korean-humanizer-research.md`](korean-humanizer-research.md) 와 [Wiki](https://github.com/dotoricode/korean-humanizer/wiki) 에 정리되어 있다.

> "AI 가 쓴 한국어는 읽으면 티가 난다. humanizer 는 그 티를 걷어낸다 — **의미는 그대로 두고 표현만**."

humanizer 는 4 가지 안전장치를 지킨다:

1. **의미 불변** — 팩트 / 숫자 / 고유명사 / 인용문 / 링크는 절대 바꾸지 않는다.
2. **20% cap** — 전체 문장 수의 20% 이상 수정하지 않는다.
3. **문단 3곳 룰** — 한 문단에 3 곳 이상 건드리지 않는다.
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

이 레포의 연구 위키( [`korean-humanizer-research.md`](korean-humanizer-research.md) ) 자체가 좋은 시연 사례다. **"AI 티가 어떻게 보이는지 설명하는 문서"** 가 그 자체로 AI 티를 가지고 있었기 때문에, 같은 위키를 humanizer 로 다듬어 [`korean-humanizer-research-humanized.md`](korean-humanizer-research-humanized.md) 에 같이 올려두었다. 아래는 Executive Summary 첫 두 단락 발췌.

**Before** *(raw — `korean-humanizer-research.md` Executive Summary)*

> 영어권에는 위키미디어 커뮤니티가 운영하는 `Signs of AI writing` 같은 집단 지식형 체크리스트가 존재하지만, 한국어권에서는 관련 지식이 국립국어원 규범 자료, 한국어 말뭉치, 그리고 최근의 ACL·EACL·국내 연구 성과에 분산되어 있다. 동시에 최근 연구는 한국어 AI 생성 텍스트 탐지가 영어 중심 방법을 그대로 이식해서는 잘 작동하지 않는다고 보여 준다. 한국어는 띄어쓰기 허용 범위가 넓고, 형태소 체계가 풍부하며, 쉼표 사용 관행과 상대 높임 체계가 영어와 다르기 때문이다. KatFish는 바로 이 점을 이용해 한국어 전용 특징을 설계했고, XDAC은 짧고 비격식적인 뉴스 댓글 영역에서 토큰·문자 수준 패턴을 끌어내어 매우 높은 탐지 성능을 보고했다.
>
> 이 문서는 그 분산된 근거를 하나의 GitHub용 한국어 레퍼런스로 통합한다. 핵심 결론은 다음과 같다. 첫째, 한국어판 “AI 작성 징후”는 단일 표현 목록이 아니라 **장르·레지스터·담화 상황을 조건으로 한 다중 신호 체계**여야 한다. 둘째, 탐지 신호 중 특히 강한 축은 **쉼표 사용 패턴**, **종결어미 및 높임법 분포**, **명사 편중과 술어·어미 부족**, **낮은 어휘 다양성**, **비격식 표지의 결핍**, **정형화된 연결어와 포맷**이다. 셋째, Humanizer는 “탐지 회피”가 아니라 **사실 보존 하의 한국어 자연화 편집기**로 설계해야 하며, 문장 종결 다양화, 연결어 절제, 명사구를 서술형으로 환원, 쉼표 감축, 맥락 허용 범위 내 생략, 비격식 표지 조절 같은 규칙을 장르별로 적용해야 한다. 넷째, 평가는 정확도만이 아니라 **오탐률, 장르 일반화, 사람 판정 일치도, 사실 보존, 윤리 통제**를 함께 보아야 한다. 최근 한국어 연구는 사람도 무보조 상태에서는 AI 여부를 간신히 구분하거나, 판단 근거를 구조화해야 일관성이 크게 개선된다고 보고한다.

**After** *(humanized — 12 카테고리 적용, 사실/숫자/고유명사/인용 보존)*

> 영어권에는 위키미디어 커뮤니티가 만든 `Signs of AI writing` 같은 집단 지식형 체크리스트가 있지만, 한국어권에서는 같은 지식이 국립국어원 규범 자료, 한국어 말뭉치, 최근의 ACL·EACL·국내 연구 성과에 흩어져 있다. 최근 연구는 한국어 AI 생성 텍스트 탐지에 영어 중심 방법을 그대로 가져다 쓰면 잘 안 된다고 본다. 한국어는 띄어쓰기 허용 범위가 넓고, 형태소 체계가 풍부하고, 쉼표 사용 관행과 상대 높임 체계가 영어와 다르다. KatFish 는 이 점을 살려 한국어 전용 특징을 설계했고, XDAC 은 짧고 비격식적인 뉴스 댓글에서 토큰·문자 수준 패턴을 끌어내 높은 탐지 성능을 보고했다.
>
> 이 문서는 흩어진 근거를 하나의 GitHub 용 한국어 레퍼런스로 모은 것이다. 핵심은 넷이다. 첫째, 한국어판 "AI 작성 징후" 는 표현 목록이 아니라 **장르·레지스터·담화 상황을 조건으로 한 다중 신호 체계**다. 둘째, 강한 신호 축은 **쉼표 사용 패턴**, **종결어미 및 높임법 분포**, **명사 편중과 술어·어미 부족**, **낮은 어휘 다양성**, **비격식 표지의 결핍**, **정형화된 연결어와 포맷**이다. 셋째, Humanizer 는 "탐지 회피" 가 아니라 **사실 보존 하의 한국어 자연화 편집기**로 설계해야 한다. 문장 종결 다양화, 연결어 절제, 명사구를 서술형으로 환원, 쉼표 감축, 맥락 허용 범위 안에서의 생략, 비격식 표지 조절 — 장르별로 다르게 쓴다. 넷째, 평가는 정확도뿐 아니라 **오탐률, 장르 일반화, 사람 판정 일치도, 사실 보존, 윤리 통제**를 함께 본다. 최근 한국어 연구는 사람도 보조 도구 없이는 AI 여부를 잘 못 가려내고, 판단 근거를 구조화해야 일관성이 올라간다고 본다.

**핵심 변화 5가지**

- "운영하는 / 존재하지만" → "만든 / 있지만" (#3 번역체·과격식)
- "분산되어 있다" → "흩어져 있다" (#6 수동태) · "그대로 이식해서는 잘 작동하지 않는다고 보여 준다" → "그대로 가져다 쓰면 잘 안 된다고 본다" (서술형 회복 + 단언)
- "동시에 / 따라서 / 뿐만 아니라 / 또한" 류 연결어 절제, 첫 줄 군더더기 제거 (#7)
- "다음과 같다 / ~여야 한다 / 적용해야 한다 / 보아야 한다" 격식 명령형 → "다 / 본다 / 쓴다" 단언형 (#11 hedging + #4 것이다)
- "매우 높은 탐지 성능을 보고했다" 의 "매우" 삭제 (#1 강조어), "이러한" 류 모두 제거 (#4)

**정량 비교**

| 지표 | Before (raw) | After (humanized) |
|---|---:|---:|
| 단락 1 글자수 | 350 | 322 |
| 단락 1 쉼표 수 | 4 | 4 |
| "또한 / 따라서 / 동시에" 연결어 (단락 1+2) | 4 | 0 |
| "이러한" 발생 | 2 | 0 |
| "~수 있다 / ~되어야 한다" 류 hedging·수동 | 6 | 1 |
| 보존된 고유명사 / 숫자 | 5 (Signs of AI writing, ACL, EACL, KatFish, XDAC) | 5 (전부 유지) |

→ 더 많은 단락 비교 + 변경 이유 + 12 카테고리 매핑: [`examples/wiki-humanized-comparison.md`](examples/wiki-humanized-comparison.md)
→ 패턴 카탈로그 적용 사례: [`examples/before-after.md`](examples/before-after.md)
→ **실제 에이전트 raw 출력 vs skill 적용 비교** (6 도메인 / 정량·정성 분석): [`examples/agent-vs-skill.md`](examples/agent-vs-skill.md)

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

### OpenCode

OpenCode 의 skills 디렉토리에 그대로 clone 한다.

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.config/opencode/skills/korean-humanizer
```

> OpenCode 는 호환을 위해 `~/.claude/skills/` 도 함께 스캔한다. Claude Code 에 이미 설치했다면 OpenCode 도 같은 경로를 자동으로 인식하므로 별도 작업이 필요 없다.

### Codex (OpenAI Codex CLI)

Codex CLI 의 skills 디렉토리에 그대로 clone 한다.

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.codex/skills/korean-humanizer
```

system prompt 형 진입을 선호하면 [`PROMPT.md`](PROMPT.md) 를 `~/.codex/AGENTS.md` 또는 프로젝트 루트의 `AGENTS.md` 끝에 append 해도 된다.

### Cursor

Cursor 는 *Rules* 또는 *시스템 프롬프트* 둘 중 하나로 진입한다.

**A. Project Rule (권장)** — 레포에 한 번만 두면 모든 대화에 적용.

```bash
mkdir -p .cursor/rules
curl -fsSL https://raw.githubusercontent.com/dotoricode/korean-humanizer/main/PROMPT.md \
  -o .cursor/rules/korean-humanizer.mdc
```

`.cursor/rules/korean-humanizer.mdc` 파일 맨 위에 다음 frontmatter 만 추가하면 된다.

```yaml
---
description: Korean humanizer — 한국어 AI 생성 텍스트의 AI 티 제거
globs: ["**/*.md", "**/*.txt"]
alwaysApply: false
---
```

**B. User Rules** — 모든 프로젝트에 적용하고 싶을 때.

`Cursor → Settings → Rules → User Rules` 에 [`PROMPT.md`](PROMPT.md) 전체 내용을 붙여 넣는다.

### ChatGPT / Gemini / 기타 LLM

[`PROMPT.md`](PROMPT.md) 전체를 시스템 프롬프트(또는 첫 메시지)에 붙여 넣고, 다듬을 한국어 텍스트를 입력하면 된다.

## Usage

### Claude Code / OpenCode / Codex

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

`PROMPT.md` 를 시스템 프롬프트(또는 Cursor Rule)에 붙여 넣은 뒤 한국어 텍스트만 입력하면 된다. 별도 명령어 없이 바로 humanize 된다.

### Personal List 캘리브레이션

자주 쓰는 금지어 / 선호어 / 유지어를 알려 주면 humanizer 가 카탈로그 패턴보다 **먼저** 적용한다. 세 가지 방식 중 편한 것을 쓰면 된다.

**1. 인라인 한 줄 (가장 빠름)** — 파일 없이 한 줄로 끝낸다.

```
/korean-humanizer 금지=활용,매우,다양한; 선호=유용하다→쓸만하다, 사실상→실제로; 유지=결과적으로

[다듬을 텍스트]
```

키워드 별칭도 인식한다. `금지`/`ban`/`avoid`, `선호`/`prefer`, `유지`/`keep` 모두 동작.

**2. 자연어 한 줄** — 형식이 부담스러우면 그냥 말로 한다.

```
/korean-humanizer

"활용", "매우" 빼고, "유용하다"는 "쓸만하다"로 바꿔서 다듬어줘:
[텍스트]
```

**3. 파일 (영구 저장이 필요할 때)** — Claude Code / OpenCode / Codex 환경에서 매번 같은 리스트를 쓸 때.

[`examples/personal-list.md`](examples/personal-list.md) 를 편집하거나, `SKILL.md` 하단의 `## My personal list` 섹션을 채운다.

세 방식 모두 동일하게 카탈로그 *앞에서* 적용된다 — 사용자 톤이 항상 우선이다.

## When Not to Apply

- 영어 / 일본어 / 중국어 등 한국어가 아닌 텍스트
- 코드, 코드 주석, 기술 문서 (정확성 우선)
- 법률 / 규제 / 공식 문서 (격식이 의도된 것)
- 단순 오탈자 / 문법 교정 (proofreading 도구가 적절)
- 사용자가 "원문 그대로" 요청한 경우

## File Structure

```
korean-humanizer/
├── README.md                                  # 이 파일
├── SKILL.md                                   # Claude Code / Cowork / OpenCode / Codex 진입점
├── PROMPT.md                                  # 일반 LLM 시스템 프롬프트 / Cursor Rule
├── LICENSE                                    # MIT
├── CONTRIBUTING.md                            # 기여 가이드
├── korean-humanizer-research.md               # 연구 근거 / feature schema / 평가 루브릭 / 윤리 (raw)
├── korean-humanizer-research-humanized.md     # 위 위키를 humanizer 로 다듬은 결과 (시연용)
├── .github/workflows/lint.yml                 # markdownlint(warning) + 패턴 표 형식 검증(fail)
├── .github/ISSUE_TEMPLATE/                    # 패턴 추가 / 도메인 사례 / 버그 보고 템플릿
├── scripts/lint-patterns.sh                   # 카테고리 표 형식 검증 (PR 안전망)
├── assets/RECORDING.md                        # 30초 데모 GIF 녹화 가이드
├── references/
│   └── ko-ai-signals.md                       # 12 카테고리 / 100+ 패턴 카탈로그 (메인 IP)
└── examples/
    ├── before-after.md                        # 패턴 카탈로그 적용 사례 (3 도메인)
    ├── agent-vs-skill.md                      # 실제 에이전트 raw vs skill 적용 비교 (6 도메인)
    ├── wiki-humanized-comparison.md           # 위키 raw ↔ humanized 단락별 상세 비교
    └── personal-list.md                       # 사용자 커스터마이징 템플릿
```

## References

- [`references/ko-ai-signals.md`](references/ko-ai-signals.md) — 12 카테고리 / 100+ 한국어 AI 패턴 카탈로그 (메인 IP)
- [`korean-humanizer-research.md`](korean-humanizer-research.md) · [Wiki](https://github.com/dotoricode/korean-humanizer/wiki) — KatFish/XDAC 등 한국어 탐지 연구 정리, feature schema, 평가 루브릭, 윤리 가이드
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

- **0.4.0** — README 최상단 hero (5초 요약 + Before/After 표) 추가, 구조 재정렬 (Overview/Categories/Full Example → Installation 위로), Wiki 배지 / 빠른 링크 / 데모 GIF placeholder, lint CI (markdownlint warning + 표 형식 검증 fail), `assets/RECORDING.md` 데모 녹화 가이드
- **0.3.1** — Full Example 을 위키 발췌(raw vs humanized) 비교로 교체, 위키 humanized 본 추가(`korean-humanizer-research-humanized.md`), 단락별 상세 비교 문서(`examples/wiki-humanized-comparison.md`) 추가
- **0.3.0** — OpenCode / Codex / Cursor 설치 가이드 분리, personal list 인라인 한 줄 입력 지원, Full Example 확장 (5문단), 연구 근거 문서(`korean-humanizer-research.md`) 추가, `references/ko-ai-signals.md` 에 KatFish/XDAC 정량 근거·feature schema·평가 루브릭 부록 추가
- **0.2.0** — 에이전트 raw 출력 vs skill 적용 비교 자료 추가 (`examples/agent-vs-skill.md`, 6 도메인 정량·정성 비교)
- **0.1.0** — 초기 공개. 12 카테고리 / 100+ 패턴 카탈로그, SKILL.md, PROMPT.md, before-after / personal-list 예제

## License

MIT — 마음대로 사용, 수정, 배포, 상업 이용 가능. 표기 의무 외엔 제한 없음.

---

*Authored by [dotoricode](https://github.com/dotoricode) · MIT License*
