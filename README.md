# korean-humanizer

> A Korean-specific AI writing humanizer for Codex and Claude Code.
>
> It removes the Korean version of "AI smell" without changing facts, names, numbers, links, or the writer's intent.

[한국어](README.ko.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v1.0--rc-orange.svg)](docs/STABILITY-PROMISE.md)
[![Patterns](https://img.shields.io/badge/patterns-137%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Domains](https://img.shields.io/badge/domains-12-brightgreen.svg)](references/ko-ai-signals.md#부록-e-도메인별-카테고리-우선-적용)
[![Korean](https://img.shields.io/badge/lang-Korean-red.svg)](references/ko-ai-signals.md)

![korean-humanizer preview](assets/translation-humanizer-card.svg)

## Try It in 30 Seconds

For a quick test, paste [`PROMPT.short.md`](PROMPT.short.md) into your LLM chat or agent instructions, then ask:

```text
Humanize this Korean text:

🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고,
이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
```

Output:

```text
이 방식으로 비즈니스 가치를 키우고, 사용자 경험도 더 좋게 만들 수 있어요.
```

Quick links: [`PROMPT.short.md`](PROMPT.short.md) · [`PROMPT.md`](PROMPT.md) · [`SKILL.md`](SKILL.md) · [`CHEATSHEET.md`](CHEATSHEET.md) · [`references/ko-ai-signals.md`](references/ko-ai-signals.md)

## Why Korean Needs Its Own Humanizer

Most AI writing humanizers are English-first. Korean has different tells:

- translation-like phrasing: `~에 있어서`, `~을 통해`, `~에 의해`
- stiff endings: `~인 것이다`, `~라고 할 수 있습니다`
- overused demonstratives: `이러한`, `해당`
- Korean LLM vocabulary: `활용`, `극대화`, `시사한다`, `도모`, `모색`
- register problems around honorifics and sentence endings
- speech text, like YouTube scripts, being flattened into written `~다` style

`korean-humanizer` is built around those Korean-specific signals instead of translating English anti-slop rules.

## What It Does

| Before | After |
|---|---|
| 🚀 **혁신적인** 솔루션을 **활용하여** **다양한** 비즈니스 **가치를 극대화**하고, **이러한 접근을 통해** 사용자 경험을 **한층 더** **고도화**할 수 있습니다. ✨ | 이 방식으로 비즈니스 가치를 키우고, 사용자 경험도 더 좋게 만들 수 있어요. |
| 지난 6개월간 **다양한** 프로젝트를 **통해** **많은 것을 배우고 성장할 수 있었던** **의미 있는** 시간이었습니다. **이러한** 경험은 앞으로의 커리어에 **있어서** **매우 소중한** 자산이 될 것이라고 **확신합니다**. 🙌 | 지난 6개월 동안 프로젝트 몇 개 하면서 많이 배웠어요. 다음에 또 써먹을 경험이라 좋았어요. |
| 본 사항은 **다양한** 측면에서 **신중하게 고려되어야** 할 필요가 있을 것으로 **사료됩니다**. | 이 건은 좀 더 봐야 할 것 같아요. |

It covers **12 categories** and **100+ Korean AI-writing patterns** across 12 domains:

blog, marketing, email, LinkedIn, YouTube, newsletter, wiki, academic writing, news, chat/DM, product reviews, and B2B messages.

## Core Rules

- **Preserve meaning.** Do not change facts, numbers, names, quotes, links, schedules, prices, or product names.
- **Edit lightly.** Do not rewrite the whole text. Fix only high-confidence AI tells.
- **Respect the 20% cap.** Edit at most 20% of sentences, with at most 3 touched spots per paragraph.
- **Handle short text carefully.** For 1-3 sentence inputs, edit at most 1 sentence.
- **Preserve Korean register.** Do not turn spoken `~해요` / `~합니다` scripts into written `~다` prose.
- **Natural beats perfect.** Slightly uneven Korean often sounds more human than polished generic copy.

## Primary Use: Codex and Claude Code

### Codex

Install as a Codex skill:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.codex/skills/korean-humanizer
```

Or append [`PROMPT.md`](PROMPT.md) to your global or project-level Codex instructions.

### Claude Code

Install as a Claude Code skill:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

Then ask naturally:

```text
이거 AI 티 빼줘:
[Korean text]
```

## Portable Prompt Use

The project is optimized for Codex and Claude Code, but the prompt files are portable:

- [`PROMPT.short.md`](PROMPT.short.md): quick copy-paste version
- [`PROMPT.md`](PROMPT.md): full system prompt with all rules
- [`SKILL.md`](SKILL.md): skill entrypoint for agent environments

Use the prompt files in any LLM environment that accepts custom instructions.

## Pattern Categories

| # | Category | Examples |
|---|---|---|
| 1 | Empty intensifiers | `매우`, `굉장히`, `한층 더` |
| 2 | Empty adjectives | `다양한`, `혁신적인`, `포괄적인` |
| 3 | Translation-ese / stiff formalism | `~에 있어서`, `~을 통해`, `다음과 같습니다` |
| 4 | `것이다` / `이러한` / `해당` overuse | `사실 ~인 것이다`, `이러한 이유로`, `해당 기능` |
| 5 | Template openings and closings | `오늘은 알아보겠습니다`, `도움이 되셨길 바랍니다` |
| 6 | Passive / hidden agents | `고려되어야 합니다`, `활용되어 왔다` |
| 7 | Filler connectives | `또한`, `뿐만 아니라`, `결론적으로` |
| 8 | Forced triplets / parallelism | `빠르고 정확하며 효율적` |
| 9 | Honorific / ending mismatch | mixed `~합니다`, `~해요`, `~다` |
| 10 | Emoji overuse | repeated section emoji / hype emoji |
| 11 | Excessive hedging | `~라고 할 수 있습니다`, `~인 것 같습니다` |
| 12 | Korean LLM vocabulary tells | `활용`, `극대화`, `시사한다`, `도모`, `모색` |

See the full catalog: [`references/ko-ai-signals.md`](references/ko-ai-signals.md).  
For a shorter reference, see [`CHEATSHEET.md`](CHEATSHEET.md).

## Customization

You can calibrate the output before the catalog rules run:

- inline bans and preferences: `금지=활용,매우; 선호=유용하다→쓸만하다`
- session-level natural language preferences
- a personal list in [`examples/personal-list.md`](examples/personal-list.md)
- a brand voice profile using frontmatter and a tone guide

Brand voice examples:

- [`examples/brand-voice-template.md`](examples/brand-voice-template.md)
- [`examples/brand-voice-toss-style.md`](examples/brand-voice-toss-style.md)
- [`examples/brand-voice-essayist.md`](examples/brand-voice-essayist.md)

## Evaluation

This repository includes a lightweight eval harness:

```bash
bash scripts/eval-harness.sh
```

It checks:

- modified sentence ratio
- per-paragraph edit cap
- length ratio
- spoken-domain `~다` intrusion
- brand voice preserve coverage

Current scorecard: [`eval/scorecard.md`](eval/scorecard.md)

## Project Map

```text
korean-humanizer/
├── README.md                     # English main README
├── README.ko.md                  # Korean README
├── README.zh-CN.md               # Simplified Chinese README
├── SKILL.md                      # Skill entrypoint
├── PROMPT.md                     # Full portable system prompt
├── PROMPT.short.md               # Short prompt for quick testing
├── CHEATSHEET.md                 # 30 common Korean AI-writing tells
├── references/ko-ai-signals.md   # Main pattern catalog
├── eval/                         # Fixtures and scorecard
├── examples/                     # Before/after and brand voice examples
├── docs/                         # Launch, migration, beta, and stability docs
└── scripts/                      # Lint and eval scripts
```

## Stability

Starting with v1.0, these surfaces are intended to remain stable across 1.x:

- 12 category names
- output format
- 20% cap / 3 spots per paragraph / spoken-domain `~다` guard
- 4-column catalog format
- Personal list and Brand voice input modes

Details: [`docs/STABILITY-PROMISE.md`](docs/STABILITY-PROMISE.md)

## Contributing

Pattern additions, domain examples, and bug reports are welcome.

Start with [`CONTRIBUTING.md`](CONTRIBUTING.md), then open an issue or PR:

- [Pattern addition](.github/ISSUE_TEMPLATE/pattern_addition.md)
- [New domain case](.github/ISSUE_TEMPLATE/new_domain_case.md)
- [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)

## Related

- [`korean-humanizer-research.md`](korean-humanizer-research.md): research notes, feature schema, evaluation rubric, ethics
- [`docs/LAUNCH.md`](docs/LAUNCH.md): copy for public release posts
- [`docs/GITHUB-TOPICS.md`](docs/GITHUB-TOPICS.md): recommended GitHub topics

## License

MIT. Use it, fork it, adapt it.
