# korean-humanizer

> Korean AI output has a recognizable tell. This removes it.

[한국어](README.ko.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable_v1.0.0-brightgreen.svg)](docs/STABILITY-PROMISE.md)
[![Patterns](https://img.shields.io/badge/patterns-137%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Domains](https://img.shields.io/badge/domains-12-brightgreen.svg)](references/ko-ai-signals.md#부록-e-도메인별-카테고리-우선-적용)

Korean text from LLMs tends to leak: stiff formalism, empty intensifiers, filler connectives that don't exist in natural speech. Readers notice. `korean-humanizer` strips those patterns — without touching the meaning.

---

```diff
# LinkedIn
- 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀
+ 이번 프로젝트에서 많이 배웠습니다. 앞으로도 도움이 될 것 같습니다.

# Email
- 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
+ 안녕하세요. 미팅 일정 때문에 연락드립니다. 일정이 겹쳐서 변경이 필요할 것 같아요.

# Marketing
- 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
+ 이 방식으로 비즈니스 가치를 키우고, 사용자 경험도 개선할 수 있습니다.
```

→ [Try it in 30 seconds](#install)

---

## Install

### Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.codex/skills/korean-humanizer
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

---

## Contributing · License · Services

Contributions welcome — [`CONTRIBUTING.md`](CONTRIBUTING.md) · [Pattern addition](.github/ISSUE_TEMPLATE/pattern_addition.md) · [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)

MIT. Use it, fork it, adapt it.

Third-party community demo by Socialistic/Tinkerland (not an official service — user input is processed by the external operator):

[![Try writing-dotoricode-korean-humanizer-5d759b on Socialistic][socialistic-demo-badge]][socialistic-demo-link]

[socialistic-demo-badge]: https://socialistic.ai/api/embed/writing-dotoricode-korean-humanizer-5d759b
[socialistic-demo-link]: https://socialistic.ai/en/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge
