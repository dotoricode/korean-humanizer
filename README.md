# korean-humanizer

> A skill and prompt for editing awkward Korean AI prose while preserving meaning.

[한국어](README.ko.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-137%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Domains](https://img.shields.io/badge/domains-12-brightgreen.svg)](references/ko-ai-signals.md#부록-e-도메인별-카테고리-우선-적용)

The latest release is **v1.0.1**. This document describes improvements on main; the next version is undecided. See the [version policy](docs/STABILITY-PROMISE.md) and [change notes](docs/UPGRADE-NOTES.md).

The catalog provides context-dependent editing candidates, not words to replace in every sentence. Preserve facts, tone, uncertainty and conditions; leave already natural text unchanged.

---

## Warp demo

Actual Codex CLI session recorded in Warp on 2026-10-07, with `korean-humanizer` as the working directory. The request, headings and explanations are in English; the original and revised email are in Korean. The generated response was not edited afterward.

[30-second video](https://github.com/dotoricode/korean-humanizer/blob/dotoricode/docs-warp-demo-media/assets/warp-demo/korean-humanizer-warp-demo-30s.mp4) · [Request screenshot](https://github.com/dotoricode/korean-humanizer/blob/dotoricode/docs-warp-demo-media/assets/warp-demo/01-request.png) · [Full result screenshot](https://github.com/dotoricode/korean-humanizer/blob/dotoricode/docs-warp-demo-media/assets/warp-demo/02-result.png)

Recorded using a local development snapshot, not a tagged release or the public main revision. The video preserves normal playback speed; see [capture details and file hashes](https://github.com/dotoricode/korean-humanizer/blob/dotoricode/docs-warp-demo-media/assets/warp-demo/provenance.json).

## Recorded model comparison

These are first final responses from native `/korean-humanizer` and `$korean-humanizer` calls on 2026-10-01. The request contains no injected skill/catalog text or answer hints. Outputs were not rewritten after the response; diff blocks extract only the response bodies. Both CLIs selected `medium` effort.

### Linkedin

**Claude Code + Opus 5.5**

```diff
- 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀
+ 이번 프로젝트에서 여러 기술적 도전을 겪으며 성장할 수 있었습니다. 이 경험은 앞으로 커리어에서 소중한 자산이 될 거라고 확신합니다.
```

**Codex CLI + GPT-6 Astra**

```diff
- 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀
+ 이번 프로젝트에서 여러 기술적 과제를 마주하며 성장할 수 있었습니다. 이 경험이 앞으로 커리어를 쌓는 데도 큰 도움이 될 거라 확신합니다.
```

### Email

**Claude Code + Opus 5.5**

```diff
- 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
+ 안녕하세요. 미팅 일정 건으로 연락드립니다. 부득이한 사정이 생겨 일정을 변경해야 합니다. 양해 부탁드립니다.
```

**Codex CLI + GPT-6 Astra**

```diff
- 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
+ 안녕하세요. 부득이한 사정으로 미팅 일정을 변경해야 해서 연락드립니다. 양해 부탁드립니다.
```

### Marketing

**Claude Code + Opus 5.5**

```diff
- 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
+ 이 솔루션으로 여러 비즈니스 가치를 최대한 끌어올리고, 사용자 경험도 더 좋게 만들 수 있습니다.
```

**Codex CLI + GPT-6 Astra**

```diff
- 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
+ 이 솔루션으로 여러 비즈니스 가치를 최대한 높이고, 사용자 경험도 더 개선할 수 있습니다.
```

[Native calls, other examples and limitations](eval/native-skill-2026-10-01.md) · [Raw first responses and hashes](eval/model-runs/native-skill-2026-10-01.json) · [Earlier direct-injection run](eval/emoji-and-flow-2026-10-01.md)

---

## Install

Run this command in the project where you want to use the skill. It uses the [Skills CLI](https://github.com/vercel-labs/skills) and requires Node.js/npm.

```bash
npx skills add dotoricode/korean-humanizer --skill korean-humanizer --agent codex claude-code --copy
```

This installs the public default branch as files in `.agents/skills/korean-humanizer/` for Codex and `.claude/skills/korean-humanizer/` for Claude Code. Use `--agent codex` or `--agent claude-code` to install for just one agent; add `--global` for all projects. The installer is a third-party CLI, not a built-in Codex or Claude command.

Start a new conversation in that project and invoke `$korean-humanizer` in Codex or `/korean-humanizer` in Claude Code, followed by your Korean text. List installed skills with `npx skills list`.

PR #5 is merged. The default branch includes improvements since v1.0.1; the latest tagged release is v1.0.1. Installation and a first invocation are checked separately from output quality; see `ROADMAP.md` for remaining release checks.

**Other LLMs:** paste [`PROMPT.short.md`](PROMPT.short.md) as a system prompt, or use the full [`PROMPT.md`](PROMPT.md).

---

## Editing rules

- Preserve facts, numbers, names, links, quotations, conditions and sentence endings.
- Rewrite awkward wording throughout the text; editing is not capped by a fixed count or percentage.
- Preserve information, conditions and certainty. Remove redundant wording without restoring it just to meet a length target.
- Use the main-branch format: `Humanized`, `주요 변경 (최대 5개)`, and the first-response revision notice.

These are instructions, not a guarantee of model compliance. Fixed-fixture checks are regression checks, not a model quality success rate. See the [evaluation guide](eval/README.md).

[Pattern catalog](references/ko-ai-signals.md) · [Quick reference](CHEATSHEET.md) · [Documentation index](docs/README.md)

---

## Customization

Ban words, set preferences, or define a brand voice — subject to meaning and tone preservation:

```text
이거 AI 티 빼줘. 금지=활용,매우; 선호=유용하다→쓸만하다:
[Korean text]
```

Load your personal file with `personal=path`; the supplied example list is not loaded automatically. For a persistent tone profile, see [`examples/brand-voice-template.md`](examples/brand-voice-template.md).

---

## Contributing · License · Services

Contributions welcome — [`CONTRIBUTING.md`](CONTRIBUTING.md) · [Pattern addition](.github/ISSUE_TEMPLATE/pattern_addition.md) · [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)

MIT. Use it, fork it, adapt it. If it helps, a GitHub Star is welcome.

Third-party community demo by Socialistic/Tinkerland (not an official service — user input is processed by the external operator):

[![Try writing-dotoricode-korean-humanizer-5d759b on Socialistic][socialistic-demo-badge]][socialistic-demo-link]

[socialistic-demo-badge]: https://socialistic.ai/api/embed/writing-dotoricode-korean-humanizer-5d759b
[socialistic-demo-link]: https://socialistic.ai/en/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge
