# korean-humanizer

> Korean AI output has a recognizable tell. This removes it.

[한국어](README.ko.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.0.1-brightgreen.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)](docs/STABILITY-PROMISE.md)
[![Patterns](https://img.shields.io/badge/patterns-137%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Domains](https://img.shields.io/badge/domains-12-brightgreen.svg)](references/ko-ai-signals.md#부록-e-도메인별-카테고리-우선-적용)

Korean text from LLMs tends to leak: stiff formalism, empty intensifiers, filler connectives that don't exist in natural speech. Readers notice. `korean-humanizer` strips those patterns — without touching the meaning.

It now also includes optional advanced passes for the cases where plain pattern replacement is not enough: voice DNA, first-line/hook cleanup, story flow, reading-load reduction, and a final anti-AI filter. These passes are conservative: they do not invent facts, rewrite the whole piece, or override the 20% edit cap.

---

```diff
# LinkedIn
- 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀
+ 이번 프로젝트에서 여러 기술적 도전을 경험했고, 그 과정에서 성장할 수 있었습니다. 이 경험은 앞으로의 커리어에도 소중한 자산이 될 것 같습니다.

# Email
- 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
+ 안녕하세요. 미팅 일정 때문에 연락드립니다. 부득이한 사정으로 일정 변경이 필요해 양해를 구하고자 합니다.

# Marketing
- 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
+ 이 솔루션으로 여러 비즈니스 가치를 더 크게 만들고, 사용자 경험도 한 단계 개선할 수 있습니다.
```

→ [Try it in 30 seconds](#install) · [Read the manual](https://docs-eta-beryl.vercel.app/korean-humanizer-manual.html)

---

## Install

### Codex

```bash
git clone https://github.com/dotoricode/korean-humanizer.git
cd korean-humanizer
bash scripts/install-codex-skill.sh
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

Then ask naturally — `이거 AI 티 빼줘:` followed by your Korean text.

**Other LLMs:** paste [`PROMPT.short.md`](PROMPT.short.md) as a system prompt, or use the full [`PROMPT.md`](PROMPT.md).

---

## Pattern Categories

| # | Category | Examples |
|---|---|---|
| 1 | Empty intensifiers | `매우`, `굉장히`, `한층 더` |
| 2 | Empty adjectives | `다양한`, `혁신적인`, `포괄적인` |
| 3 | Translation-ese / stiff formalism | `~에 있어서`, `~을 통해`, `다음과 같습니다` |
| 4 | `것이다` / `이러한` / `해당` overuse | `사실 ~인 것이다`, `이러한 이유로` |
| 5 | Template openings and closings | `오늘은 알아보겠습니다`, `도움이 되셨길 바랍니다` |
| 6 | Passive / hidden agents | `고려되어야 합니다`, `활용되어 왔다` |
| 7 | Filler connectives | `또한`, `뿐만 아니라`, `결론적으로` |
| 8 | Forced triplets / parallelism | `빠르고 정확하며 효율적` |
| 9 | Honorific / ending mismatch | mixed `~합니다`, `~해요`, `~다` |
| 10 | Emoji overuse | repeated section emoji / hype emoji |
| 11 | Excessive hedging | `~라고 할 수 있습니다`, `~인 것 같습니다` |
| 12 | Korean LLM vocabulary tells | `활용`, `극대화`, `시사한다`, `도모` |

Full catalog: [`references/ko-ai-signals.md`](references/ko-ai-signals.md) · Quick reference: [`CHEATSHEET.md`](CHEATSHEET.md)

---

## Customization

Ban words, set preferences, or define a brand voice — all applied before the catalog runs:

```text
이거 AI 티 빼줘. 금지=활용,매우; 선호=유용하다→쓸만하다:
[Korean text]
```

For a persistent tone profile, see [`examples/brand-voice-template.md`](examples/brand-voice-template.md).

For a personal writing fingerprint built from your own samples, see [`examples/voice-dna-template.md`](examples/voice-dna-template.md) and [`examples/voice-dna-extraction.md`](examples/voice-dna-extraction.md).

## Advanced Passes

The stable surface is still the 12 Korean AI-tell categories. Advanced passes sit on top as optional, conservative checks:

| Pass | What it fixes | Guardrail |
|---|---|---|
| Voice DNA | Output drifts away from the user's own sentence shapes and anti-voice | Never imitates a third party without user-provided samples |
| Hook / first line | Topic arrives late or opener is vague | First 1-2 sentences only; no clickbait |
| Story flow | Body reads like "and then / also / additionally" stacking | Uses only relationships already present in the draft |
| Dumbify | Dense clauses, abstract nouns, avoidable jargon | Lowers reading load, not the idea |
| Anti-AI final | Hollow contrast, inflated claims, generic authority | Specificity without invented numbers or events |

---

## Contributing · License · Services

Contributions welcome — [`CONTRIBUTING.md`](CONTRIBUTING.md) · [Pattern addition](.github/ISSUE_TEMPLATE/pattern_addition.md) · [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)

MIT. Use it, fork it, adapt it.

Third-party community demo by Socialistic/Tinkerland (not an official service — user input is processed by the external operator):

[![Try writing-dotoricode-korean-humanizer-5d759b on Socialistic][socialistic-demo-badge]][socialistic-demo-link]

[socialistic-demo-badge]: https://socialistic.ai/api/embed/writing-dotoricode-korean-humanizer-5d759b
[socialistic-demo-link]: https://socialistic.ai/en/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge
